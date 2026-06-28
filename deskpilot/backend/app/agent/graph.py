from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import reason_node, tool_node, tool_tracker_node, should_continue

builder = StateGraph(AgentState)

builder.add_node("reason", reason_node)
builder.add_node("tools", tool_node)
builder.add_node("track", tool_tracker_node)

builder.set_entry_point("reason")

builder.add_conditional_edges(
    "reason",
    should_continue,
    {"tools": "tools", "end": END},
)
builder.add_edge("tools", "track")
builder.add_edge("track", "reason")

graph = builder.compile()
