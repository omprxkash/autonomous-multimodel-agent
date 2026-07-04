# model-router

A lightweight LLM dispatcher that routes tasks to the right model based on task type, then invokes it and returns the response with cost and latency metadata.

---

## What it does

Instead of hardcoding a single model across every project, `model-router` lets you declare what *kind* of task you have — classification, summarisation, reasoning, generation, or coding — and the router picks the model that best fits: fast and cheap for simple tasks, capable for complex ones.

Every response includes estimated cost in USD and measured latency, so you can track spend and performance without instrumenting each project separately.

---

## Routing table

| Task type | Provider | Model | Temperature |
|---|---|---|---|
| `classification` | Gemini | gemini-2.0-flash | 0.0 |
| `summarisation` | Gemini | gemini-2.0-flash | 0.3 |
| `reasoning` | Gemini | gemini-2.0-flash | 0.3 |
| `generation` | OpenAI | gpt-4o | 0.7 |
| `coding` | OpenAI | gpt-4o | 0.2 |

Unknown task types fall back to `reasoning`.

---

## API

### Invoke a model

```
POST /invoke
```

```json
{
  "task_type": "summarisation",
  "content": "Summarise this text...",
  "max_tokens": 512,
  "temperature": null
}
```

Response:

```json
{
  "provider": "gemini",
  "model": "gemini-2.0-flash",
  "response": "...",
  "input_tokens": 142,
  "output_tokens": 87,
  "estimated_cost_usd": 0.0000369,
  "latency_ms": 834.2
}
```

### List routing config

```
GET /models
```

Returns the full routing table — which model each task type maps to.

### Health check

```
GET /health
```

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| LLM (Gemini) | langchain-google-genai |
| LLM (OpenAI) | langchain-openai |
| Container | Docker |

---

## Quick start

```bash
cd model-router
cp .env.example .env
# Fill in GEMINI_API_KEY and/or OPENAI_API_KEY
docker compose up --build
# API available at http://localhost:8001
```

---

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | For Gemini routes | Google Gemini API key |
| `OPENAI_API_KEY` | For OpenAI routes | OpenAI API key |
| `DEFAULT_PROVIDER` | No (default: `gemini`) | Fallback provider if neither key is set |

---

## Calling from another service

```python
import httpx

resp = httpx.post("http://model-router:8001/invoke", json={
    "task_type": "classification",
    "content": "Classify this email as spam or not spam: ...",
    "max_tokens": 64,
})
result = resp.json()
print(result["response"], result["estimated_cost_usd"])
```

---

## Project structure

```
model-router/
├── app/
│   ├── __init__.py
│   ├── config.py      Pydantic Settings (API keys, default provider)
│   ├── models.py      RouteRequest / RouteResponse Pydantic models
│   ├── router.py      ROUTING_TABLE, COST_TABLE, select_route(), invoke()
│   └── main.py        FastAPI app — /invoke, /models, /health
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```
