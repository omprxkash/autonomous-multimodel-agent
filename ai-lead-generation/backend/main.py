from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command

from routers import leads, pipeline, templates
from routers.followups import router as followups_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield


app = FastAPI(
    title="Lead Pipeline API",
    description="B2B lead-generation pipeline — scrape, enrich, score, draft.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads.router)
app.include_router(pipeline.router)
app.include_router(templates.router)
app.include_router(followups_router)


@app.get("/health")
def health():
    return {"status": "ok"}

