# Multi-Step Agent

An autonomous agentic pipeline framework for orchestrating complex, multi-step workflows using LLMs as the core reasoning engine.

---

## What it is

A multi-step agent accepts a high-level goal, breaks it into an ordered sequence of subtasks, executes each subtask using the right tools, and synthesises the results into a final output — without requiring human intervention at each step.

Unlike a single-turn LLM call, a multi-step agent maintains state across steps, retries on failure, and loops through a reasoning cycle until the task is complete.

---

## Why it matters

Most real-world problems are not single-step. They require pulling data from multiple sources, transforming it, making decisions from intermediate results, and producing structured outputs. Businesses have a strong need to automate large portions of repetitive, multi-stage work — and a well-built multi-step agent handles this as a continuous reasoning loop rather than a series of disconnected API calls.

---

## Architecture

```
Input (goal / task)
        │
        ▼
┌────────────────────────────────────┐
│           Task Planner             │  ← LLM decomposes goal into subtasks
└────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────┐
│          Execution Loop            │
│                                    │
│  Step N:                           │
│    reason → select tool            │
│    → execute → observe             │
│    → update state → next step      │
└────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────┐
│        Output Synthesiser          │  ← aggregates step results into final answer
└────────────────────────────────────┘
        │
        ▼
  Final Output
```

---

## Core components

### Task Planner
Accepts a high-level goal and decomposes it into an ordered list of subtasks. Uses an LLM with a structured output schema to produce the plan.

### State Manager
Maintains shared context across all steps — what has been completed, what intermediate results are available, and what still needs to happen. Every node reads from and writes to this shared state.

### Tool Executor
Maps each subtask to the right tool (web search, database query, API call, code execution, file read/write, etc.) and handles retries on tool failure before surfacing an error upstream.

### Output Synthesiser
Takes the accumulated state after all steps complete and produces the final structured output — a report, a decision, an action, or a generated artefact.

### Human-in-the-loop Gate
An optional node that surfaces proposed actions for human approval before execution. Essential when the agent has write access — sending emails, creating records, or triggering external side effects.

---

## Example workflow: content research pipeline

| Step | What happens |
|---|---|
| 1. Search | Pull articles, papers, and discussions on a topic from multiple sources |
| 2. Filter | Score results for relevance against a target audience profile |
| 3. Summarise | Extract key points from each source |
| 4. Synthesise | Combine summaries into a structured outline |
| 5. Generate | Produce a first draft from the outline |

Each step is a node in the graph. The agent loops between steps until the task is complete, retrying failed steps before escalating.

---

## Stack

| Layer | Technology |
|---|---|
| Agent orchestration | LangGraph |
| LLM backbone | Gemini 2.0 Flash / Claude Sonnet (switchable) |
| Tool execution | LangChain ToolNode |
| State | LangGraph StateGraph (TypedDict) |
| Backend | FastAPI |
| Storage | PostgreSQL |
| Containers | Docker Compose |

---

## Key design principles

**Stateful, not stateless** — the agent carries context forward between steps instead of restarting from scratch each time.

**Tool-first reasoning** — the LLM decides which tool to use at each step; it does not generate answers from memory alone.

**Graceful degradation** — if a tool fails, the agent retries with a fallback strategy rather than halting the entire pipeline.

**Inspectable** — every step, its inputs, outputs, and the LLM's reasoning trace are logged for debugging and downstream evaluation.

---

## Use cases

- Automated research and report generation
- Multi-source data aggregation pipelines
- Business process automation — lead enrichment, customer triage, document processing
- Personalised content creation pipelines
- Autonomous monitoring and alerting workflows
- Any workflow where a human currently follows a repeatable multi-step process

---

## Project structure

```
multi-step-agent/
├── backend/
│   ├── app/
│   │   ├── main.py               FastAPI entry point
│   │   ├── agent/
│   │   │   ├── graph.py          LangGraph StateGraph definition
│   │   │   ├── nodes.py          All node implementations (planner, executor, synthesiser)
│   │   │   ├── state.py          AgentState TypedDict
│   │   │   └── tools.py          Tool definitions
│   │   ├── core/
│   │   │   ├── config.py         Settings
│   │   │   └── database.py       SQLAlchemy setup
│   │   └── routers/
│   │       └── tasks.py          API endpoints for submitting and monitoring tasks
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── components/
│           ├── TaskSubmit.jsx     Goal input and pipeline trigger
│           ├── StepTrace.jsx      Live step-by-step execution view
│           └── OutputPanel.jsx    Final synthesised output
├── docker-compose.yml
└── .env.example
```
