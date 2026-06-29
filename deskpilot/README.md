# deskpilot

An autonomous agentic "Chief of Staff" that integrates with Google Workspace (Gmail/Calendar) to manage tasks, schedules, and communications with long-term semantic memory.

---

## What it does

- **Chat interface** — conversational access to your entire workspace
- **Gmail** — search threads, read emails, compose drafts (shows you the draft before sending)
- **Calendar** — check availability, draft and create events (confirms before writing)
- **Persistent memory** — learns your preferences, constraints, and context across conversations via pgvector semantic search
- **Human-in-the-loop** — every write action is surfaced as an editable draft block; nothing sends without your confirmation

---

## Agent loop

The ReAct loop runs on LangGraph:

```
User message
    → Memory retrieval (semantic + importance-based, pgvector L2)
    → Gemini reasons: tool needed or direct reply?
    → Tool execution (Gmail / Calendar API, on-demand OAuth refresh)
    → Draft returned to UI for confirmation
    → Memory update (LLM-extracted facts stored for future sessions)
```

**Edge cases handled:**
- OAuth token expired → refreshed on-demand from stored refresh_token, no re-auth prompt
- Gemini quota hit → surfaces a clear error message, does not crash silently
- Empty memory (cold start) → skips retrieval, proceeds with system context only
- Very long input → truncated to 4000 chars before embedding
- Draft rejected by user → agent rewrites without executing the previous version

---

## Stack

| Layer | Technology |
|---|---|
| Agent | LangGraph (ReAct), Gemini 2.0 Flash |
| Backend | FastAPI, SQLAlchemy async, asyncpg |
| Memory | PostgreSQL + pgvector, embedding-001 (768 dims) |
| Auth | Google OAuth 2.0 (refresh token stored), JWT HS256 |
| Frontend | Next.js 14 App Router, TypeScript, ReactMarkdown |
| Infra | Docker Compose |

---

## File structure

```
deskpilot/
├── backend/
│   ├── app/
│   │   ├── main.py                     # lifespan: pgvector extension + inline migrations
│   │   ├── api/
│   │   │   ├── auth.py                 # OAuth login/callback, setup, profile
│   │   │   ├── chat.py                 # conversation, message, memory endpoints
│   │   │   └── integrations.py         # direct Gmail + Calendar API endpoints
│   │   ├── agent/
│   │   │   ├── graph.py                # LangGraph StateGraph (reason → tools → track)
│   │   │   ├── nodes.py                # reason_node, tool_node, tool_tracker_node
│   │   │   ├── tools.py                # Gmail + Calendar tool definitions
│   │   │   └── state.py                # AgentState TypedDict
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py             # asyncpg URL auto-conversion
│   │   │   └── security.py             # JWT helpers
│   │   ├── models/
│   │   │   ├── user.py                 # refresh_token, is_setup_complete, job_title, main_goal
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   └── memory.py               # MemoryFact (fact, category, importance) + MemoryEmbedding (Vector 768)
│   │   └── services/
│   │       ├── gmail_service.py        # on-demand credentials from refresh_token
│   │       ├── calendar_service.py     # on-demand credentials from refresh_token
│   │       └── memory_service.py       # MemoryGraph, extract_facts, hybrid retrieval
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx                # full chat UI: onboarding, sidebar, drafts, toasts
│   │       ├── auth/callback/page.tsx
│   │       ├── layout.tsx
│   │       └── globals.css             # glassmorphism: bg-mesh, typing-dot, toast, modal
│   └── package.json
├── docker-compose.yml
├── .env.example
└── .gitignore
```

---

## Setup

**1. Google Cloud project**

1. Create a project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable **Gmail API** and **Google Calendar API**
3. Create OAuth 2.0 credentials (Web application)
4. Add authorised redirect URI: `http://localhost:8000/auth/callback`

**2. Clone and configure**

```bash
git clone https://github.com/omprxkash/autonomous-multimodel-agent.git
cd autonomous-multimodel-agent/deskpilot
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=change-me-before-production
DATABASE_URL=postgresql://deskpilot:deskpilot@postgres:5432/deskpilot
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
GEMINI_API_KEY=your-gemini-api-key
FRONTEND_URL=http://localhost:3000
```

**3. Start all services**

```bash
docker compose up --build
```

Starts: `postgres` (with pgvector), `backend` (FastAPI on 8000), `frontend` (Next.js on 3000).

**4. Sign in**

Go to `http://localhost:3000` → "Sign in with Google" → complete the onboarding (name, job title, main goal) → start chatting.

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/auth/login` | Returns `{"auth_url": "..."}` for Google OAuth |
| `GET` | `/auth/callback` | Exchanges code, redirects to frontend with token |
| `POST` | `/auth/setup` | Onboarding: name, job_title, main_goal, work_hours |
| `POST` | `/chat/message` | Send message, get agent reply |
| `GET` | `/chat/conversations` | List conversations |
| `GET` | `/chat/memories` | List stored memory facts |
| `GET` | `/gmail/inbox/{user_id}` | Fetch inbox |
| `GET` | `/calendar/events/{user_id}` | Fetch upcoming events |

---

## Draft pattern

When the agent decides to send an email or create a calendar event, it returns a draft block instead of executing immediately:

**Email draft:**
```
--- DRAFT START ---
To: alice@company.com
Subject: Project sync Thursday
Body:
Hi Alice — just confirming our Thursday sync at 2 PM.
Let me know if that time still works.
--- DRAFT END ---
```

**Calendar draft:**
```
--- CALENDAR START ---
Title: Project sync with Alice
Date: Thursday, 3 July 2025
Time: 14:00
Description: Weekly project check-in
--- CALENDAR END ---
```

The UI renders these as interactive cards. Edit the text directly, then click **Send** or **Confirm event** — or **Discard** to abort. The agent does not proceed without explicit confirmation.

---

## Memory

Memory is extracted from every conversation automatically. The LLM parses each message into structured facts:

```json
{
  "fact": "User prefers meetings after 10 AM",
  "category": "preference",
  "importance": 0.9
}
```

Facts are embedded with `embedding-001` (768 dims) and stored in pgvector. Retrieval is hybrid: semantic similarity (L2 distance) + importance ranking, deduplicated. The agent uses these to personalise every reply without being told the same thing twice.

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | yes | JWT signing secret (HS256) |
| `DATABASE_URL` | yes | PostgreSQL connection string |
| `GOOGLE_CLIENT_ID` | yes | OAuth app ID |
| `GOOGLE_CLIENT_SECRET` | yes | OAuth app secret |
| `GOOGLE_REDIRECT_URI` | yes | Must match Google Console exactly |
| `GEMINI_API_KEY` | yes | Gemini API key |
| `FRONTEND_URL` | yes | Base URL for OAuth redirect |
| `DEBUG` | no | Set `true` to enable /docs |
