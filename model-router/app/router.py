import time
from app.models import RouteRequest, RouteResponse

ROUTING_TABLE = {
    "classification": {"provider": "gemini", "model": "gemini-2.0-flash", "temperature": 0.0},
    "summarisation":  {"provider": "gemini", "model": "gemini-2.0-flash", "temperature": 0.3},
    "reasoning":      {"provider": "gemini", "model": "gemini-2.0-flash", "temperature": 0.3},
    "generation":     {"provider": "openai", "model": "gpt-4o",           "temperature": 0.7},
    "coding":         {"provider": "openai", "model": "gpt-4o",           "temperature": 0.2},
}

# Cost per 1K tokens (approximate, USD)
COST_TABLE = {
    ("gemini", "gemini-2.0-flash"): {"input": 0.000075, "output": 0.0003},
    ("openai", "gpt-4o"):           {"input": 0.0025,   "output": 0.01},
    ("openai", "gpt-4o-mini"):      {"input": 0.00015,  "output": 0.0006},
}


def select_route(task_type: str) -> dict:
    return ROUTING_TABLE.get(task_type, ROUTING_TABLE["reasoning"])


def invoke(request: RouteRequest) -> RouteResponse:
    from langchain_core.messages import HumanMessage
    from app.config import settings

    route = select_route(request.task_type)
    provider = route["provider"]
    model = route["model"]
    temperature = request.temperature if request.temperature is not None else route["temperature"]

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            max_output_tokens=request.max_tokens,
            google_api_key=settings.GEMINI_API_KEY,
        )
    else:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=request.max_tokens,
            openai_api_key=settings.OPENAI_API_KEY,
        )

    t0 = time.time()
    result = llm.invoke([HumanMessage(content=request.content)])
    latency_ms = (time.time() - t0) * 1000

    response_text = result.content
    usage = getattr(result, "usage_metadata", None) or {}
    input_tokens = usage.get("input_tokens", 0) if isinstance(usage, dict) else getattr(usage, "input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0) if isinstance(usage, dict) else getattr(usage, "output_tokens", 0)

    cost_rates = COST_TABLE.get((provider, model), {"input": 0.0, "output": 0.0})
    estimated_cost = (input_tokens / 1000) * cost_rates["input"] + (output_tokens / 1000) * cost_rates["output"]

    return RouteResponse(
        provider=provider,
        model=model,
        response=response_text,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost_usd=estimated_cost,
        latency_ms=latency_ms,
    )
