# autonomous-multimodel-agent

Autonomous AI agent systems — multi-model orchestration and real-world agentic pipelines.

---

## Projects

### Autonomous Multi-Model Agent
An orchestration layer that routes tasks across multiple LLMs based on capability, cost, and latency. Agents plan, delegate subtasks, call tools, and synthesise results — with a shared memory layer so context persists across turns and across models.

### `ai-lead-generation/`
A B2B lead-generation pipeline built as an agentic workflow: scrapes company pages, scores prospects against an ideal customer profile, drafts personalised outreach emails, and tracks the full pipeline on a Kanban board. Uses a weighted rule-based scoring model with per-factor breakdowns — no black-box scoring.

```
Scrape → Enrich → Score → Draft outreach → Track (Kanban)
```

Key features: offline mode with mock company pages · transparent ICP scoring · Jinja2 outreach templates · drag-and-drop pipeline board · full Docker setup

---

## Stack
Python · LangChain · LangGraph · FastAPI · React · Docker
