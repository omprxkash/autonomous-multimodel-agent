# deskpilot

An autonomous agentic "Chief of Staff" that integrates with Google Workspace (Gmail/Calendar) to manage tasks, schedules, and communications with long-term semantic memory.

A production-grade AI Chief of Staff platform built with Python (LangGraph), Next.js, and AWS. Features context-aware memory, Google Workspace integration (Gmail/Calendar), and deployable cloud infrastructure.

---

## What it does

- **Chat interface** — conversational access to your workspace (streaming SSE + fallback REST)
- **Gmail** — search threads, read emails, compose drafts (sends only after you confirm)
- **Calendar** — check free/busy windows, draft and create events
- **Persistent memory** — learns your preferences across conversations via pgvector semantic search
- **Human-in-the-loop** — all write actions (emails, events) surface as interactive draft cards before execution
- **Intent classification** — 6-node LangGraph graph classifies query/action/chat before routing
- **AI reply suggestions** — three AI-generated reply drafts (quick / standard / detailed) for any email

---

## Architecture

```
Browser ──SSE──▶ /api/stream/chat
                       │
              LangGraph 6-node agent
                       │
         ┌─────────────┼─────────────┐
  classify_intent  retrieve_memory  memory_updater
         │               │               │
       reason ◀──────── tools ──────── track
         │
      Gemini 2.0 Flash (or OpenAI, switchable)
         │
    Gmail API / Calendar API
```

### Agent graph nodes

| Node | Role |
|---|---|
| `classify_intent` | Tags message as `query`, `action`, or `chat` |
| `retrieve_memory` | Loads relevant semantic memories from pgvector |
| `reason` | Main LLM node — decides tool calls or direct reply |
| `tools` | LangGraph `ToolNode` executing Gmail / Calendar tools |
| `track` | Increments tool call counter (max 10 per turn) |
| `memory_updater` | Extracts new preferences/facts and stores them |

---

## Stack

| Layer | Technology |
|---|---|
| Agent | LangGraph ReAct, Gemini 2.0 Flash / OpenAI GPT-4 (switchable) |
| Backend | FastAPI, SQLAlchemy async, asyncpg |
| Memory | PostgreSQL + pgvector (768-dim or 1536-dim embeddings) |
| Cache | Redis (in-memory fallback when Redis unavailable) |
| Auth | Google OAuth 2.0, JWT HS256, 7-day expiry |
| Frontend | Next.js 14 App Router, Tailwind CSS, glassmorphism UI |
| Streaming | Server-Sent Events (`/api/stream/chat`) |
| Infra | Docker Compose (dev), AWS ECS + RDS + ElastiCache + ALB (prod) |
| IaC | Terraform (VPC, ECR, ECS, RDS pg16, ElastiCache, ALB) |
| CI/CD | GitHub Actions (lint + build on PR, build+push+deploy on main) |

---

## File structure

```
deskpilot/
├── backend/
│   ├── app/
│   │   ├── main.py               FastAPI app + lifespan migrations
│   │   ├── api/
│   │   │   ├── auth.py           Google OAuth 2.0 flow
│   │   │   ├── chat.py           REST chat endpoint + conversation history
│   │   │   ├── stream.py         SSE streaming chat endpoint
│   │   │   ├── users.py          /users/me compatibility shim
│   │   │   ├── email.py          AI reply suggestions + send
│   │   │   └── calendar.py       Create event + list events
│   │   ├── agent/
│   │   │   ├── graph.py          6-node LangGraph StateGraph
│   │   │   ├── nodes.py          All 6 node implementations
│   │   │   ├── state.py          AgentState TypedDict
│   │   │   └── tools.py          Gmail + Calendar tool definitions
│   │   ├── core/
│   │   │   ├── config.py         Pydantic Settings (Gemini/OpenAI/Redis/JWT)
│   │   │   ├── database.py       Async SQLAlchemy engine
│   │   │   └── security.py       JWT encode/decode
│   │   ├── models/
│   │   │   ├── user.py           User table
│   │   │   ├── conversation.py   Conversation + ChatMessage tables
│   │   │   └── memory.py         MemoryFact + MemoryEmbedding tables
│   │   ├── services/
│   │   │   ├── gmail.py          Gmail API service
│   │   │   ├── calendar.py       Calendar API service
│   │   │   ├── memory_service.py pgvector semantic memory retrieval
│   │   │   ├── embeddings.py     Embedding generation (Gemini/OpenAI)
│   │   │   └── cache.py          Redis cache with in-memory fallback
│   │   └── utils/
│   │       └── token_refresh.py  OAuth token refresh logic
│   ├── init-pgvector.sql         Loaded by Postgres container at startup
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── page.tsx           Landing + onboarding
│       │   ├── dashboard/page.tsx ChiefAI-style 3-column dashboard
│       │   ├── auth/callback/     OAuth callback handler
│       │   └── globals.css        Glassmorphism theme
│       ├── components/
│       │   ├── Chat.tsx           SSE streaming chat with message formatter
│       │   ├── IntegrationPanel.tsx  Gmail/Calendar connection status
│       │   ├── CalendarWidget.tsx    7-day event preview
│       │   ├── ComposeEmailDialog.tsx  New email compose modal
│       │   ├── EmailReplyDialog.tsx    AI reply suggestions modal
│       │   └── ui/
│       │       ├── email-card.tsx
│       │       ├── event-card.tsx
│       │       ├── draft-card.tsx
│       │       ├── action-card.tsx
│       │       └── free-time-card.tsx
│       └── config/api.ts
├── .github/workflows/
│   ├── ci.yml                 Lint + build on every PR
│   └── deploy.yml             Build → ECR → ECS deploy on main
├── terraform/
│   ├── main.tf                VPC, ECR, RDS pg16, ElastiCache, ALB, ECS cluster
│   ├── variables.tf
│   └── outputs.tf
├── deployment/
│   └── deploy.sh              Manual one-shot ECS deployment
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Draft markers

The agent uses two marker formats (both supported):

```
***EMAIL_DRAFT***
To: recipient@example.com
Subject: Re: your message
Body…
***END_EMAIL_DRAFT***
```

```
***EVENT_PROPOSAL***
Title: Team sync
Start: 2026-01-15T10:00:00
End: 2026-01-15T11:00:00
***END_EVENT_PROPOSAL***
```

Cortex-style markers (`--- DRAFT START ---`) are also detected by the frontend for backward compatibility.

---

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/auth/login` | Start Google OAuth flow |
| GET | `/api/auth/callback` | OAuth callback, issues JWT |
| GET | `/api/auth/me` | Current user info |
| POST | `/api/chat/message` | REST chat (non-streaming) |
| GET | `/api/chat/conversations` | List conversation history |
| POST | `/api/stream/chat` | **SSE streaming chat** |
| GET | `/api/users/me` | Deprecated — use `/api/auth/me` |
| POST | `/api/email/suggest-replies` | 3 AI-generated reply drafts |
| POST | `/api/email/send` | Send email via Gmail |
| GET | `/api/calendar/events` | List upcoming events |
| POST | `/api/calendar/create` | Create calendar event |

---

## Quick start (local)

```bash
# 1. Clone and enter the project
cd deskpilot

# 2. Backend environment
cp .env.example backend/.env
# Fill in GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GEMINI_API_KEY, SECRET_KEY

# 3. Start everything
docker compose up --build

# 4. Open http://localhost:3000
```

The Postgres container automatically loads `init-pgvector.sql` which runs `CREATE EXTENSION IF NOT EXISTS vector` before any tables are created.

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GOOGLE_CLIENT_ID` | Yes | — | OAuth 2.0 client ID |
| `GOOGLE_CLIENT_SECRET` | Yes | — | OAuth 2.0 client secret |
| `GOOGLE_REDIRECT_URI` | No | `http://localhost:8000/api/auth/callback` | OAuth callback URL |
| `GEMINI_API_KEY` | Yes* | — | Google Gemini API key |
| `OPENAI_API_KEY` | No | — | OpenAI API key (if using OpenAI provider) |
| `ACTIVE_LLM_PROVIDER` | No | `gemini` | `gemini` or `openai` |
| `DATABASE_URL` | No | local default | `postgresql+asyncpg://...` |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Falls back to in-memory if unavailable |
| `SECRET_KEY` | Yes | — | JWT signing secret |
| `FRONTEND_URL` | No | `http://localhost:3000` | Used in OAuth redirect |

---

## Memory system

Memories are stored in two tables:
- `memory_facts` — content, category (preference / habit / project / contact), importance score
- `memory_embeddings` — pgvector 768-dim vectors from `embedding-001`

Retrieval uses cosine/L2 similarity to surface the top-5 most relevant facts before each reasoning turn. The `memory_updater` node runs a lightweight LLM extraction after every turn to store new preferences stated by the user.

---

## Production deployment

```bash
# Provision infrastructure
cd terraform
terraform init
terraform apply -var-file=prod.tfvars

# Deploy containers (after pushing images to ECR)
./deployment/deploy.sh
```

The GitHub Actions `deploy.yml` workflow automates this on every push to `main`: builds Docker images, pushes to ECR, and triggers ECS rolling deploys.
