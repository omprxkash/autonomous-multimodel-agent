from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import RouteRequest, RouteResponse
from app.router import ROUTING_TABLE, invoke

app = FastAPI(title="model-router", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/invoke", response_model=RouteResponse)
def invoke_model(request: RouteRequest):
    try:
        return invoke(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
def list_models():
    return ROUTING_TABLE


@app.get("/health")
def health():
    return {"status": "ok"}
