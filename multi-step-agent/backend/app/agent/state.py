from __future__ import annotations
from typing import Optional, List
from typing_extensions import TypedDict


class StepLog(TypedDict):
    step: str
    status: str
    output: Optional[str]
    error: Optional[str]


class AgentState(TypedDict):
    goal: str
    search_queries: List[str]
    search_results: List[dict]
    filtered_results: List[dict]
    summaries: List[str]
    outline: str
    draft: str
    step_logs: List[StepLog]
    current_step: str
    status: str
    error: Optional[str]
