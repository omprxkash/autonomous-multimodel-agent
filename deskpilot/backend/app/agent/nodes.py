from datetime import datetime, timezone
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, ToolMessage, AIMessage
from langgraph.prebuilt import ToolNode
from app.core.config import settings
from app.agent.state import AgentState
from app.agent.tools import ALL_TOOLS

MAX_TOOL_CALLS = 10

_llm = None


def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.3,
        ).bind_tools(ALL_TOOLS)
    return _llm


def build_system_prompt(state: AgentState) -> str:
    return (
        f"You are deskpilot, a personal workspace assistant.\n"
        f"Current time: {state['current_time']}\n\n"
        f"Personalization: {state['personalization']}\n\n"
        f"Relevant memory context:\n{state['memory_context'] or 'No prior context.'}\n\n"
        "Guidelines:\n"
        "- For emails and calendar events, always generate a DRAFT first and wait for user confirmation before sending.\n"
        "- Extract and remember important facts from conversations (names, preferences, projects).\n"
        "- Be concise unless the user asks for detail.\n"
        "- If a tool fails, explain what happened and suggest alternatives.\n"
    )


def reason_node(state: AgentState) -> dict:
    if state.get("tool_calls_made", 0) >= MAX_TOOL_CALLS:
        return {
            "messages": [AIMessage(content="I've reached the maximum number of tool calls for this turn. Please try again.")],
        }

    llm = get_llm()
    system = SystemMessage(content=build_system_prompt(state))
    response = llm.invoke([system] + state["messages"])
    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return "end"


tool_node = ToolNode(ALL_TOOLS)


def tool_tracker_node(state: AgentState) -> dict:
    return {"tool_calls_made": state.get("tool_calls_made", 0) + 1}
