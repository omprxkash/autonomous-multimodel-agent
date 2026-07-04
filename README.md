> For system architecture and how all projects connect — [ARCHITECTURE.md](ARCHITECTURE.md)

# autonomous-multimodel-agent

Autonomous AI agent systems — multi-model orchestration and real-world agentic pipelines.

---

## Projects

### `model-router/`
A shared LLM dispatcher that routes tasks to the right model based on task type, cost, and latency. Classification tasks go to fast/cheap models; reasoning and generation tasks go to capable ones. Exposes a `/invoke` API that any project in this repo can call instead of hitting a model directly.

```
Task → Classify type → Select model → Invoke → Return response + cost metadata
```

---

### `multi-step-agent/`
An autonomous content research pipeline. Given a research goal, the agent plans search queries, fetches web results, filters by relevance, summarises each source, builds an outline, and writes a first draft — all without human intervention at each step.

```
Planner → Search → Filter → Summarise → Outline → Draft
```

Key features: LangGraph straight-chain graph · DuckDuckGo search (no API key) · step-by-step trace visible in the dashboard · React frontend with live step status · Docker setup

---

### `deskpilot/`
An autonomous AI Chief of Staff that integrates with Google Workspace (Gmail + Calendar). Reads and drafts emails, manages your calendar, learns your preferences via semantic memory, and surfaces phishing risk scores on incoming mail.

```
Gmail / Calendar → LangGraph 6-node agent → Draft card (human confirms before send)
```

Key features: LangGraph ReAct loop · Gemini 2.0 Flash / OpenAI switchable · pgvector semantic memory · SSE streaming chat · Gmail push notifications (Pub/Sub webhook) · mail-phis risk scoring on inbox · AWS ECS + Terraform IaC · GitHub Actions CI/CD

---

### `ai-lead-generation/`
A B2B lead-generation pipeline: scrapes company pages, scores prospects against an ideal customer profile, drafts personalised outreach emails, tracks the full pipeline on a Kanban board, and schedules automatic follow-up sequences.

```
Scrape → Enrich → Score → Draft outreach → Send → Follow-up sequences → Track (Kanban)
```

Key features: transparent ICP scoring (industry / size / seniority / tech / geo) · Jinja2 outreach templates · follow-up scheduling with stage tracking · drag-and-drop pipeline board · full Docker setup

---

### `mail-phis/`
SOC-grade phishing detection pipeline for email and URL analysis. Parses raw MIME messages through a 9-stage forensic pipeline — authentication verification, URL threat intelligence, NLP social engineering detection, and attachment risk scoring — and returns a structured verdict with an exportable IOC bundle.

```
Raw email → 9-stage pipeline → Verdict (SAFE / MARKETING / SUSPICIOUS / PHISHING) + IOC bundle
```

Key features: dual-bucket risk scoring (suspicion − trust, 0–100) · content-only NLP capped at SUSPICIOUS · STIX2-compatible IOC export · concurrent threat intel (OpenPhish / PhishTank / URLhaus) · RTLO + homograph detection · async redirect chain tracing

---

## Stack

Python · LangGraph · LangChain · FastAPI · React · Next.js · PostgreSQL · Redis · Celery · Docker