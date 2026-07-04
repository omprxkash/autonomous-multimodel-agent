from __future__ import annotations
import json
import re
import httpx
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from app.agent.state import AgentState, StepLog

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        if settings.ACTIVE_LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
            from langchain_openai import ChatOpenAI
            _llm = ChatOpenAI(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=0.3,
            )
        else:
            from langchain_google_genai import ChatGoogleGenerativeAI
            _llm = ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.3,
                convert_system_message_to_human=True,
            )
    return _llm


def _parse_json_response(text: str):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    return json.loads(text)


def _fetch_page(url: str) -> str:
    try:
        resp = httpx.get(url, timeout=10, follow_redirects=True)
        from selectolax.parser import HTMLParser
        tree = HTMLParser(resp.text)
        parts = []
        for node in tree.css("p, article"):
            t = node.text(strip=True)
            if t:
                parts.append(t)
        return " ".join(parts)[:3000]
    except Exception:
        return ""


def _search_duckduckgo(query: str) -> list[dict]:
    try:
        from duckduckgo_search import DDGS
        results = DDGS().text(query, max_results=5)
        return [{"url": r["href"], "title": r["title"], "snippet": r["body"]} for r in results]
    except Exception:
        return []


async def planner_node(state: AgentState) -> dict:
    llm = _get_llm()
    messages = [
        SystemMessage(content=(
            "You are a research assistant. Given a research goal, generate 3 to 5 specific web search queries "
            "that will help gather comprehensive information on the topic.\n"
            "Respond with ONLY a JSON array of strings, no explanation. Example: [\"query one\", \"query two\"]"
        )),
        HumanMessage(content=f"Research goal: {state['goal']}"),
    ]
    response = await llm.ainvoke(messages)
    queries = _parse_json_response(response.content)
    log: StepLog = {"step": "planner", "status": "complete", "output": f"Generated {len(queries)} queries", "error": None}
    return {
        "search_queries": queries,
        "current_step": "search",
        "step_logs": state.get("step_logs", []) + [log],
    }


async def search_node(state: AgentState) -> dict:
    results = []
    for query in state["search_queries"]:
        results.extend(_search_duckduckgo(query))
        if len(results) >= 20:
            break
    results = results[:20]
    log: StepLog = {"step": "search", "status": "complete", "output": f"Found {len(results)} results", "error": None}
    return {
        "search_results": results,
        "current_step": "filter",
        "step_logs": state.get("step_logs", []) + [log],
    }


async def filter_node(state: AgentState) -> dict:
    llm = _get_llm()
    results = state["search_results"]
    numbered = "\n".join(
        f"{i}. {r['title']}: {r['snippet'][:200]}"
        for i, r in enumerate(results)
    )
    messages = [
        SystemMessage(content=(
            "You are a relevance filter. Given a research goal and a list of search results, "
            "return the 0-based indices of the top 5 most relevant results as a JSON array of integers. "
            "Respond with ONLY the JSON array."
        )),
        HumanMessage(content=f"Goal: {state['goal']}\n\nResults:\n{numbered}"),
    ]
    response = await llm.ainvoke(messages)
    indices = _parse_json_response(response.content)
    indices = [i for i in indices if isinstance(i, int) and 0 <= i < len(results)][:5]
    filtered = [results[i] for i in indices]
    log: StepLog = {"step": "filter", "status": "complete", "output": f"Kept {len(filtered)} results", "error": None}
    return {
        "filtered_results": filtered,
        "current_step": "summarise",
        "step_logs": state.get("step_logs", []) + [log],
    }


async def summarise_node(state: AgentState) -> dict:
    llm = _get_llm()
    summaries = []
    for result in state["filtered_results"]:
        page_text = _fetch_page(result["url"])
        content = page_text if page_text else result["snippet"]
        messages = [
            SystemMessage(content=(
                "You are a research summariser. Extract 3 to 5 key bullet points from the provided text "
                "that are most relevant to the research goal. Be concise and factual."
            )),
            HumanMessage(content=f"Goal: {state['goal']}\n\nSource: {result['title']}\n\n{content}"),
        ]
        response = await llm.ainvoke(messages)
        summaries.append(response.content.strip())
    log: StepLog = {"step": "summarise", "status": "complete", "output": f"Summarised {len(summaries)} sources", "error": None}
    return {
        "summaries": summaries,
        "current_step": "outline",
        "step_logs": state.get("step_logs", []) + [log],
    }


async def outline_node(state: AgentState) -> dict:
    llm = _get_llm()
    all_summaries = "\n\n".join(
        f"Source {i + 1}:\n{s}" for i, s in enumerate(state["summaries"])
    )
    messages = [
        SystemMessage(content=(
            "You are a content strategist. Based on the research summaries, create a structured outline "
            "for a comprehensive article. Use H2 headings (##) for main sections and bullet points for sub-topics. "
            "The outline should logically flow and cover the research goal thoroughly."
        )),
        HumanMessage(content=f"Goal: {state['goal']}\n\nSummaries:\n{all_summaries}"),
    ]
    response = await llm.ainvoke(messages)
    outline = response.content.strip()
    log: StepLog = {"step": "outline", "status": "complete", "output": "Outline created", "error": None}
    return {
        "outline": outline,
        "current_step": "draft",
        "step_logs": state.get("step_logs", []) + [log],
    }


async def draft_node(state: AgentState) -> dict:
    llm = _get_llm()
    messages = [
        SystemMessage(content=(
            "You are a professional writer. Using the provided outline, write a complete, well-structured "
            "first draft article of approximately 500 words. Write in clear, engaging prose. "
            "Use the outline headings and expand each section with substance."
        )),
        HumanMessage(content=f"Goal: {state['goal']}\n\nOutline:\n{state['outline']}"),
    ]
    response = await llm.ainvoke(messages)
    draft = response.content.strip()
    log: StepLog = {"step": "draft", "status": "complete", "output": "Draft written", "error": None}
    return {
        "draft": draft,
        "status": "complete",
        "current_step": "done",
        "step_logs": state.get("step_logs", []) + [log],
    }
