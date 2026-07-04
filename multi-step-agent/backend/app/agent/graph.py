from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import planner_node, search_node, filter_node, summarise_node, outline_node, draft_node

builder = StateGraph(AgentState)
builder.add_node("planner", planner_node)
builder.add_node("search", search_node)
builder.add_node("filter", filter_node)
builder.add_node("summarise", summarise_node)
builder.add_node("outline", outline_node)
builder.add_node("draft", draft_node)
builder.set_entry_point("planner")
builder.add_edge("planner", "search")
builder.add_edge("search", "filter")
builder.add_edge("filter", "summarise")
builder.add_edge("summarise", "outline")
builder.add_edge("outline", "draft")
builder.add_edge("draft", END)
graph = builder.compile()
