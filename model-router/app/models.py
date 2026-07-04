from typing import Optional
from pydantic import BaseModel


class RouteRequest(BaseModel):
    task_type: str  # "classification" | "reasoning" | "generation" | "coding" | "summarisation"
    content: str
    max_tokens: int = 1024
    temperature: Optional[float] = None


class RouteResponse(BaseModel):
    provider: str
    model: str
    response: str
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float
    latency_ms: float
