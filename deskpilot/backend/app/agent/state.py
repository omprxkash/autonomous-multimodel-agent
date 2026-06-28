from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    conversation_id: str
    memory_context: str
    personalization: str
    current_time: str
    pending_draft: dict | None
    tool_calls_made: int
