![mail-phis tests](https://github.com/omprxkash/autonomous-multimodel-agent/actions/workflows/test-mail-phis.yml/badge.svg)

# autonomous-multimodel-agent

Five production-grade AI projects forming a complete, layered agent infrastructure — from routing and pipelines to workspace automation, phishing detection, and outreach.

For architecture and cross-project connections → [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Projects

### `model-router/`
Shared LLM dispatcher. Routes by task type (classification, summarisation, reasoning, generation, coding), picks the right model, and returns the response with token count, cost estimate, and latency. Rate-limited at 30 req/min per IP.

```
Task type → Select model + provider → Invoke → Response + cost + latency
```

**Stack:** FastAPI · langchain-google-genai · langchain-openai · slowapi · Docker

---

### `multi-step-agent/`
Autonomous content research pipeline built on LangGraph. Given a goal, the agent plans searches, fetches results, filters by relevance, summarises each source, builds an outline, and drafts the final piece — no human steps between them.

```
Planner → Search → Filter → Summarise → Outline → Draft
```

**Stack:** LangGraph · DuckDuckGo search · FastAPI · React · Docker

---

### `deskpilot/`
AI Chief of Staff with Google Workspace integration. Reads and drafts emails, manages calendar, stores preferences in semantic memory, and flags phishing risk on every inbox message.

```
Gmail / Calendar → LangGraph 6-node ReAct agent → Draft (human confirms before send)
```

**Key features:** pgvector semantic memory · SSE streaming · Gmail Pub/Sub push notifications · mail-phis inbox scoring · OpenTelemetry tracing · MCP server (search_gmail, read_email, list_calendar_events) · AWS ECS + Terraform IaC

**Stack:** LangGraph · FastAPI · pgvector · Google OAuth · OpenTelemetry · Terraform · Docker

---

### `ai-lead-generation/`
B2B outreach pipeline: scrapes company pages, scores prospects against a weighted ICP (industry, company size, seniority, tech stack, geography), drafts personalised emails with Jinja2 or an LLM, tracks leads on a Kanban board, and schedules follow-up sequences automatically.

```
Scrape → Enrich → ICP score → Draft email → Kanban → Follow-up sequences
```

**Key features:** transparent per-factor score breakdown · LLM email drafting (Gemini / GPT-4o, set `use_llm=true`) · Celery Beat follow-up scheduling · optional SendGrid delivery · end-to-end demo script (`scripts/demo.py`)

**Stack:** FastAPI · LangChain · Celery · SQLAlchemy · React · Docker

---

### `mail-phis/`
SOC-grade phishing detection for raw MIME email. Nine-stage forensic pipeline: header analysis, SPF/DKIM/DMARC verification, URL threat intelligence, domain age, homograph detection, NLP social-engineering scoring, attachment risk, dual-bucket scoring, IOC export.

```
Raw MIME → 9-stage pipeline → Verdict (SAFE / MARKETING / SUSPICIOUS / PHISHING) + IOC bundle
```

**Key features:** dual-bucket scoring (suspicion − trust, 0–100) · content-only NLP capped at SUSPICIOUS · STIX2 IOC export · concurrent OpenPhish / PhishTank / URLhaus lookups · 16 pytest tests (CI passing)

**Stack:** FastAPI · asyncpg · Celery · Docker

---

## Stack

| Layer | Technology |
|---|---|
| Agent framework | LangGraph · LangChain |
| API | FastAPI |
| Database | PostgreSQL · pgvector · SQLAlchemy |
| Background tasks | Celery · Redis |
| Frontend | React · Next.js |
| Observability | OpenTelemetry |
| Infrastructure | Docker · Terraform · AWS ECS |