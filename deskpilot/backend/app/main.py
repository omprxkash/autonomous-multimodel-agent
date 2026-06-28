import logging
import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, chat, integrations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("deskpilot")

ORIGINS = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://localhost:8000",
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initialising database and pgvector...")
    async with engine.begin() as conn:
        # pgvector extension — must exist before any vector column is created
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        # --- schema migrations (safe to re-run) ---
        for stmt in [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_setup_complete INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS job_title VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS main_goal TEXT",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS work_hours VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE memory_facts ADD COLUMN IF NOT EXISTS metadata_json TEXT",
            "ALTER TABLE memory_facts ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS conversation_id UUID",
        ]:
            try:
                await conn.execute(text(stmt))
            except Exception as exc:
                logger.warning("Migration skipped: %s", exc)

        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database ready.")
    yield
    await engine.dispose()


app = FastAPI(
    title="deskpilot",
    description="Agentic workspace assistant",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.middleware("http")
async def error_middleware(request: Request, call_next):
    """Preserve CORS headers even on unhandled 500s."""
    try:
        return await call_next(request)
    except Exception as exc:
        logger.error("Unhandled exception: %s\n%s", exc, traceback.format_exc())
        origin = request.headers.get("origin", "")
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Credentials": "true",
        }
        if origin in ORIGINS:
            headers["Access-Control-Allow-Origin"] = origin
        return Response(
            content=f'{{"detail": "Internal server error"}}',
            status_code=500,
            headers=headers,
        )


app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(integrations.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "deskpilot"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, proxy_headers=True, forwarded_allow_ips="*")
