# System Architecture

This repository contains five production-grade AI projects that form a complete, layered AI engineering system. Each project works independently but they are designed to connect.

---

## The system in one picture

```
                        ┌─────────────────────────────┐
                        │        model-router          │  ← shared LLM dispatcher
                        │   routes by task type,       │     (cost + latency routing)
                        │   returns cost + latency      │
                        └────────────┬────────────────┘
                                     │ called by
              ┌──────────────────────┼─────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
   ┌─────────────────┐   ┌────────────────────┐  ┌──────────────────────┐
   │  multi-step-    │   │     deskpilot       │  │   ai-lead-           │
   │  agent          │   │  AI Chief of Staff  │  │   generation         │
   │  (pipeline      │   │  Gmail + Calendar   │  │   B2B outreach       │
   │   framework)    │   │  LangGraph 6-node   │  │   pipeline           │
   └─────────────────┘   └────────┬────────────┘  └──────────────────────┘
                                  │ scores inbox
                                  ▼
                        ┌─────────────────┐
                        │   mail-phis     │  ← phishing detection
                        │   9-stage       │     feeds into deskpilot
                        │   forensic pipe │
                        └─────────────────┘

          ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
          All agents above can be submitted to eval-harness-system
          (see omprxkash/eval-harness-system) for quality scoring
```

---

## The five layers

### Layer 1 — Routing infrastructure: `model-router/`

Sits between your application code and the LLM providers. You tell it what *kind* of task you have; it picks the right model (fast/cheap for classification, capable for generation), invokes it, and returns the response with token count, cost, and latency.

Any project that calls an LLM can route through this service instead of hardcoding a model.

**When to look at this project:** LLM routing, cost optimisation, provider abstraction, FastAPI microservices.

---

### Layer 2 — Generic pipeline framework: `multi-step-agent/`

A content research pipeline built on LangGraph. The architecture is the point: planner → search → filter → summarise → outline → draft as a straight-chain StateGraph with no ReAct loop. Each step is a node; the agent carries state forward between them.

This pattern applies to any workflow where a goal decomposes into an ordered sequence of subtasks — lead enrichment, report generation, document processing.

**When to look at this project:** LangGraph straight-chain graphs, DuckDuckGo tool integration, step-trace dashboards, React polling UI.

---

### Layer 3 — Intelligent workspace agent: `deskpilot/`

The most complete agent in the system. A LangGraph 6-node ReAct loop (classify intent → retrieve memory → reason → tools → track → update memory) with Google Workspace integration (Gmail + Calendar), pgvector semantic memory, SSE streaming, JWT auth, and production infrastructure (Terraform + GitHub Actions CI/CD).

Calls `mail-phis` to score each incoming email before surfacing it in the inbox. Can optionally route LLM calls through `model-router`.

**When to look at this project:** LangGraph ReAct loops, semantic memory (pgvector), Google OAuth, SSE streaming, AWS ECS + Terraform IaC, GitHub Actions.

---

### Layer 4 — Security pipeline: `mail-phis/`

A phishing detection engine that parses raw MIME email through a 9-stage forensic pipeline: header analysis → SPF/DKIM/DMARC verification → URL analysis → domain intelligence → threat intelligence (OpenPhish/PhishTank/URLhaus) → NLP content scoring → attachment risk → dual-bucket scoring → IOC export.

No LLM involved — entirely classical: deterministic rules, threat feed lookups, Levenshtein distance for homograph detection.

**When to look at this project:** Security engineering, forensic pipelines, STIX2 IOC formats, dual-bucket scoring engines, classical NLP for threat signals.

---

### Layer 5 — Lead generation pipeline: `ai-lead-generation/`

B2B outreach pipeline: HTML scraping → lead enrichment → weighted ICP scoring (industry/size/seniority/tech/geo) → Jinja2 email drafting → Kanban tracking → follow-up scheduling with Celery Beat and optional SendGrid delivery.

The ICP scorer is transparent — every score comes with a per-factor breakdown so you can see exactly why a lead scored what it did.

**When to look at this project:** Rule-based scoring engines, Jinja2 templating, Celery Beat scheduling, Kanban UI with drag-and-drop.

---

## Cross-project connections

| From | To | How |
|---|---|---|
| `deskpilot` | `mail-phis` | `GET /email/inbox` fetches each email's raw bytes and POSTs to `mail-phis /api/analyze/email` |
| `deskpilot` | `model-router` | Can swap direct Gemini/OpenAI calls for `POST model-router/invoke` with task_type |
| `ai-lead-generation` | `model-router` | Same — ICP email drafting can route through model-router |
| Any agent | `eval-harness-system` | POST the agent's run trace to `agent-evaluator /api/runs` for quality scoring |

---

## Skill map — where to look for what

| Skill area | Project |
|---|---|
| LangGraph ReAct loop + memory | `deskpilot/` |
| LangGraph straight-chain pipeline | `multi-step-agent/` |
| LLM routing + cost tracking | `model-router/` |
| Google OAuth + Gmail API | `deskpilot/` |
| Forensic security pipeline | `mail-phis/` |
| Rule-based scoring with breakdown | `ai-lead-generation/` |
| Celery + Beat scheduling | `ai-lead-generation/` |
| AWS ECS + Terraform IaC | `deskpilot/` |
| GitHub Actions CI/CD | `deskpilot/` |
| Agent evaluation and self-correction | → `omprxkash/eval-harness-system` |

---

## Related repository

**[omprxkash/eval-harness-system](https://github.com/omprxkash/eval-harness-system)** — the quality assurance layer for this system. Contains `agent-evaluator` (LLM-as-judge eval harness with Celery pipeline, failure classification, correction generation) and `review-automation` (classical NLP baseline with no LLM dependency).
