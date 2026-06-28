# deskpilot

An agentic workspace assistant that connects to your Gmail and Google Calendar. It reads, searches, and drafts emails or events on your behalf — but always shows you a draft before sending anything.

## What it does

- **Chat interface** — conversational access to your workspace
- **Gmail** — search threads, read emails, compose drafts (sends only after you confirm)
- **Calendar** — check free/busy windows, draft and create events
- **Persistent memory** — learns your preferences across conversations using vector similarity
- **Human-in-the-loop** — drafts are surfaced as visible blocks before any write action executes

## Stack

| Layer | Technology |
|---|---|
| Agent | LangGraph (ReAct loop), Gemini 2.0 Flash |
| Backend | FastAPI, SQLAlchemy async, asyncpg |
| Memory | PostgreSQL + pgvector, embedding-001 (768 dims) |
| Auth | Google OAuth 2.0, JWT HS256 |
| Frontend | Next.js 14 App Router, TypeScript |
| Infra | Docker Compose |

## Quick start

```bash
cp .env.example .env
# fill in GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GEMINI_API_KEY, SECRET_KEY

docker compose up --build
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8000/docs`

### Local dev (without Docker)

```bash
# backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend
cd frontend
npm install
npm run dev
```

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | yes | JWT signing secret |
| `DATABASE_URL` | yes | asyncpg connection string |
| `GOOGLE_CLIENT_ID` | yes | Google OAuth app ID |
| `GOOGLE_CLIENT_SECRET` | yes | Google OAuth secret |
| `GOOGLE_REDIRECT_URI` | yes | Must match Google Console |
| `GEMINI_API_KEY` | yes | Gemini API key |
| `FRONTEND_URL` | yes | Base URL for OAuth redirects |

## API

| Method | Path | Description |
|---|---|---|
| `GET` | `/auth/login` | Start Google OAuth flow |
| `GET` | `/auth/callback` | OAuth callback, returns JWT |
| `GET` | `/auth/me` | Current user info |
| `POST` | `/chat/message` | Send message, get agent reply |
| `GET` | `/chat/conversations` | List past conversations |
| `GET` | `/chat/conversations/{id}/messages` | Load conversation history |

## Draft pattern

When the agent composes an email or creates a calendar event, it returns a structured draft block rather than executing immediately:

```
--- DRAFT START ---
Type: email
To: alice@example.com
Subject: Team sync tomorrow
Body:
Hi Alice — just confirming our sync at 10am tomorrow.
--- DRAFT END ---
```

Reply "send it", "looks good", or similar to confirm. Say "cancel" or "rewrite" to discard.
