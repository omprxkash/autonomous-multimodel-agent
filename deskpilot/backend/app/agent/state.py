from typing import Annotated, TypedDict, Optional, List, Dict, Any
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # Core conversation
    messages: Annotated[list, add_messages]
    user_id: str
    conversation_id: str
    session_id: str

    # Context injected at start of each turn
    memory_context: str
    personalization: str
    current_time: str

    # Intent classification (classify_intent node)
    intent: Optional[str]        # "query" | "action" | "chat"
    needs_tools: bool

    # Memory retrieval (retrieve_memory node)
    retrieved_memories: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]

    # Tool execution tracking (cortex-style ReAct loop)
    tool_calls_made: int

    # Draft state (for human-in-the-loop email/event confirmation)
    pending_draft: Optional[Dict[str, Any]]

    # Memory updates extracted after response (memory_updater node)
    new_memories: List[Dict[str, Any]]

    # Final streamed response (populated by response_generator, used by SSE)
    response: Optional[str]
