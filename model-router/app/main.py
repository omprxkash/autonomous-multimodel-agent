from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.models import RouteRequest, RouteResponse
from app.router import ROUTING_TABLE, invoke

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="model-router", version="1.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/invoke", response_model=RouteResponse)
@limiter.limit("30/minute")
def invoke_model(request: Request, body: RouteRequest):
    try:
        return invoke(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
def list_models():
    return ROUTING_TABLE


@app.get("/health")
def health():
    return {"status": "ok"}
