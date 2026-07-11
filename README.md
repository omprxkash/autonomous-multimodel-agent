![mail-phis tests](https://github.com/omprxkash/autonomous-multimodel-agent/actions/workflows/test-mail-phis.yml/badge.svg)

# autonomous-multimodel-agent

Six AI projects: a complete, layered agent infrastructure — routing, pipelines, workspace automation, phishing detection, outreach — plus an autonomous multi-agent company-builder experiment.

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

### `company-builder/`
Autonomous company-building experiment: one goal prompt takes an orchestrator agent from open-internet pain research to a finished go-to-market package with no human input mid-run. The run produced **ReconStock** (a safety-first Shopify inventory-sync concept): verified market research, an idea tournament with adversarial fact-checking, business plan, brand identity, a working product demo + landing page, launch/founder videos, and a red-team report — every claim traced to a fetched URL or disclosed in an honesty log.

```
Pain hunt (8 parallel researchers) → Tournament + adversarial verification → Business design → Brand → Build + verify → Videos → Red team → Package
```

**Key features:** multi-agent orchestration (parallel researchers, judge panels, skeptic verifiers, fresh-eyes auditor) · self-correction (caught its own misattributed stat and synthetic evidence) · 34-check Playwright end-to-end verification · fully local video production (Playwright screen recording + TTS + ffmpeg) · decision + honesty logs · start at `company-builder/run-1/RECAP.html`

**Stack:** Claude Code multi-agent orchestration · Playwright · Node · ffmpeg-static

---

## Core pattern

Every agent in this repo runs a ReAct loop — Reason, Act, Observe, repeat. The LangGraph
graphs are structured expressions of this loop. The bare-API version makes the mechanics explicit:

```python
messages = [{"role": "user", "content": task}]

while True:
    response = client.messages.create(model=..., tools=tools, messages=messages)
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        return final_answer(response)

    tool_results = [run_tool(block) for block in response.content if block.type == "tool_use"]
    messages.append({"role": "user", "content": tool_results})
```

`messages` is the agent's memory — every tool call and result is appended so the LLM always
sees the full history of what it has done. LangGraph replaces the `while` loop with a
`StateGraph`, tool dispatch with `ToolNode`, and the stop condition with an `END` edge —
same loop, more structure.

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