"""
LangGraph agent graph — 6-node merged pattern.

classify_intent → retrieve_memory → reason ←→ [tools → track]
                                         ↓
                                   memory_updater → END
"""
from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    classify_intent_node,
    retrieve_memory_node,
    reason_node,
    tool_node,
    tool_tracker_node,
    memory_updater_node,
    should_use_tools,
)

builder = StateGraph(AgentState)

builder.add_node("classify_intent", classify_intent_node)
builder.add_node("retrieve_memory", retrieve_memory_node)
builder.add_node("reason", reason_node)
builder.add_node("tools", tool_node)
builder.add_node("track", tool_tracker_node)
builder.add_node("memory_updater", memory_updater_node)

builder.set_entry_point("classify_intent")

builder.add_edge("classify_intent", "retrieve_memory")
builder.add_edge("retrieve_memory", "reason")

# After reasoning: either call tools (ReAct loop) or update memory and exit
builder.add_conditional_edges(
    "reason",
    should_use_tools,
    {"tools": "tools", "memory_updater": "memory_updater"},
)

# Tool call loop: tools → track → reason
builder.add_edge("tools", "track")
builder.add_edge("track", "reason")

builder.add_edge("memory_updater", END)

graph = builder.compile()
