from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.database import init_db, engine
from app.core.telemetry import setup_telemetry
from app.api import auth, chat
from app.api import stream, users, email, calendar
from app.api.webhooks import router as webhooks_router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Enable pgvector and run inline schema migrations before table creation
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        for stmt in [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_setup_complete INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS job_title VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS main_goal TEXT",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS work_hours VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE memory_facts ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS conversation_id_col UUID",
        ]:
            try:
                await conn.execute(text(stmt))
            except Exception as exc:
                pass  # column already exists or table not yet created
    setup_telemetry()
    await init_db()
    yield


app = FastAPI(
    title="deskpilot",
    description=(
        "An autonomous agentic Chief of Staff that integrates with Google Workspace "
        "(Gmail/Calendar) to manage tasks, schedules, and communications with "
        "long-term semantic memory."
    ),
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    lifespan=lifespan,
)

FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core routes
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

# Streaming SSE
app.include_router(stream.router, prefix="/api")

# ChiefAI-pattern compatibility routes
app.include_router(users.router, prefix="/api")
app.include_router(email.router, prefix="/api")
app.include_router(calendar.router, prefix="/api")
app.include_router(webhooks_router, prefix="/api")
