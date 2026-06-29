"""
LangGraph agent nodes — merged cortex ReAct loop + ChiefAI 6-node pattern.

Graph shape:
  classify_intent → retrieve_memory → reason [→ tools → track → reason] → memory_updater → END
"""
import json
import re
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ChatPromptTemplate
from langgraph.prebuilt import ToolNode
from app.core.config import settings
from app.agent.state import AgentState
from app.agent.tools import ALL_TOOLS

MAX_TOOL_CALLS = 10

_llm = None
_llm_plain = None  # unbound, for classification and memory tasks


def _build_llm(bind_tools: bool = True):
    if settings.ACTIVE_LLM_PROVIDER == "openai" and settings.OPENAI_API_KEY:
        from langchain_openai import ChatOpenAI
        base = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=0.3,
        )
    else:
        from langchain_google_genai import ChatGoogleGenerativeAI
        key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        base = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=key,
            temperature=0.3,
            convert_system_message_to_human=True,
        )
    return base.bind_tools(ALL_TOOLS) if bind_tools else base


def get_llm():
    global _llm
    if _llm is None:
        _llm = _build_llm(bind_tools=True)
    return _llm


def get_llm_plain():
    global _llm_plain
    if _llm_plain is None:
        _llm_plain = _build_llm(bind_tools=False)
    return _llm_plain


# ---------------------------------------------------------------------------
# Node 1 — classify_intent (ChiefAI)
# ---------------------------------------------------------------------------

async def classify_intent_node(state: AgentState) -> dict:
    """Classify user intent: 'query', 'action', or 'chat'."""
    last_message = state["messages"][-1]

    classification_prompt = [
        SystemMessage(content="""You are an intent classifier for a personal workspace AI assistant.

Classify the user's message into ONE of:
- query   : needs to CHECK Gmail or Calendar data
- action  : needs to PERFORM an action (send email, create/modify/delete event, draft reply)
- chat    : general conversation, preferences, or questions that don't need external data

Respond with ONLY the category name: query, action, or chat"""),
        HumanMessage(content=last_message.content if hasattr(last_message, "content") else str(last_message)),
    ]

    try:
        response = await get_llm_plain().ainvoke(classification_prompt)
        intent = response.content.strip().lower()
        if intent not in ("query", "action", "chat"):
            intent = "chat"
    except Exception:
        intent = "chat"

    needs_tools = intent in ("query", "action")
    return {"intent": intent, "needs_tools": needs_tools}


# ---------------------------------------------------------------------------
# Node 2 — retrieve_memory (ChiefAI)
# ---------------------------------------------------------------------------

async def retrieve_memory_node(state: AgentState) -> dict:
    """Fetch relevant memories and populate user_preferences / memory_context."""
    # memory_context is already pre-populated by chat.py before graph invocation;
    # this node is a no-op enrichment hook — downstream nodes can override it.
    return {
        "retrieved_memories": [],
        "user_preferences": {"context_str": state.get("memory_context", "")},
    }


# ---------------------------------------------------------------------------
# Node 3 — reason (cortex) — main ReAct reasoning node
# ---------------------------------------------------------------------------

def _build_system_prompt(state: AgentState) -> str:
    intent = state.get("intent", "chat")
    memory = state.get("memory_context") or ""
    prefs = (state.get("user_preferences") or {}).get("context_str", "")
    context = prefs or memory

    now = datetime.now(timezone.utc)
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (now + timedelta(days=7)).strftime("%Y-%m-%d")

    return (
        f"You are deskpilot, an autonomous Chief-of-Staff AI with access to Gmail and Google Calendar.\n"
        f"Current time: {state.get('current_time', now.isoformat())}\n"
        f"Detected intent: {intent}\n\n"
        f"User context:\n{context or 'No prior context.'}\n\n"
        f"Date helpers: tomorrow={tomorrow}, next_week={next_week}\n\n"
        "Guidelines:\n"
        "- For emails and calendar events, produce a DRAFT marked with ***EMAIL_DRAFT*** ... ***END_EMAIL_DRAFT***\n"
        "  or ***EVENT_PROPOSAL*** ... ***END_EVENT_PROPOSAL*** before executing.\n"
        "- Extract and remember user preferences mentioned in conversation.\n"
        "- Be concise unless the user asks for detail.\n"
        "- If a tool fails, explain what happened and suggest an alternative.\n"
        "- Never fabricate email content or calendar data.\n"
    )


async def reason_node(state: AgentState) -> dict:
    """Main reasoning node — decides whether to call tools or respond directly."""
    if state.get("tool_calls_made", 0) >= MAX_TOOL_CALLS:
        return {
            "messages": [AIMessage(content="Maximum tool calls reached for this turn. Please try again.")],
            "response": "Maximum tool calls reached for this turn. Please try again.",
        }

    system = SystemMessage(content=_build_system_prompt(state))
    response = await get_llm().ainvoke([system] + list(state["messages"]))

    updates: dict = {"messages": [response]}
    if not (hasattr(response, "tool_calls") and response.tool_calls):
        updates["response"] = response.content
    return updates


# ---------------------------------------------------------------------------
# Node 4 — tools (cortex ToolNode)
# ---------------------------------------------------------------------------

tool_node = ToolNode(ALL_TOOLS)


# ---------------------------------------------------------------------------
# Node 5 — tool_tracker (cortex)
# ---------------------------------------------------------------------------

def tool_tracker_node(state: AgentState) -> dict:
    return {"tool_calls_made": state.get("tool_calls_made", 0) + 1}


# ---------------------------------------------------------------------------
# Node 6 — memory_updater (ChiefAI)
# ---------------------------------------------------------------------------

_PREF_PATTERNS = [
    (r"\b(?:i\s+(?:don'?t|hate|dislike|prefer\s+not\s+to)\s+(?:have|hold|take)\s+\w+\s+meetings?)\b", "preference"),
    (r"\b(?:i\s+(?:prefer|like|love|enjoy)\s+\w+\s+meetings?)\b", "preference"),
    (r"\bwork\s+from\s+(?:home|office)\b", "fact"),
]


def _extract_simple_memories(text: str) -> list[dict]:
    memories = []
    lower = text.lower()
    for pattern, mem_type in _PREF_PATTERNS:
        if re.search(pattern, lower):
            memories.append({"content": text[:120], "type": mem_type})
            break
    return memories


async def memory_updater_node(state: AgentState) -> dict:
    """
    Extract new facts/preferences from the latest user message and store them.
    Uses a lightweight LLM extraction as a best-effort pass.
    """
    last_user_msg = next(
        (m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)),
        None,
    )
    if not last_user_msg:
        return {"new_memories": []}

    content = last_user_msg.content if hasattr(last_user_msg, "content") else ""

    # Fast rule-based pass first
    new_memories = _extract_simple_memories(content)

    if not new_memories and len(content.split()) >= 3:
        try:
            extraction_prompt = [
                SystemMessage(content="""Extract user preferences or facts from the message.
Return JSON: {"preferences": ["..."], "facts": ["..."]}
If nothing to extract, return {"preferences": [], "facts": []}
ONLY respond with JSON."""),
                HumanMessage(content=content[:500]),
            ]
            resp = await get_llm_plain().ainvoke(extraction_prompt)
            raw = resp.content.strip()
            # Strip markdown fences if present
            raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE)
            extracted = json.loads(raw)
            for pref in extracted.get("preferences", []):
                new_memories.append({"content": pref, "type": "preference"})
            for fact in extracted.get("facts", []):
                new_memories.append({"content": fact, "type": "fact"})
        except Exception:
            pass

    return {"new_memories": new_memories}


# ---------------------------------------------------------------------------
# Routing helpers
# ---------------------------------------------------------------------------

def should_use_tools(state: AgentState) -> str:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and getattr(last, "tool_calls", None):
        return "tools"
    return "memory_updater"
