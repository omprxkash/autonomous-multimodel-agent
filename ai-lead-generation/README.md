# ai-lead-generation

**A personal B2B lead-generation pipeline — scrape company pages, score prospects against your ideal customer profile, draft outreach emails, and manage everything on a Kanban board.**

I built this because I was tired of managing leads in spreadsheets and copy-pasting the same outreach email with minor tweaks. The whole thing runs locally with Docker, uses a bundled set of mock company pages so it works offline, and keeps the scoring completely transparent — you can see exactly why a lead scored the way it did, broken down by factor.

---

## What it does

1. **Scrapes** company pages (or reads bundled mock pages offline) to pull out the name, domain, industry, headcount, location, tech stack, and a contact.
2. **Enriches** the raw data — normalises industry categories, derives a company size bucket, identifies seniority from job title, validates the email format.
3. **Scores** each lead against your Ideal Customer Profile using a weighted rule-based model. Every score comes with a per-factor breakdown so nothing is a black box.
4. **Drafts a personalised outreach email** using Jinja2 templates with merge fields — the right tone and angle based on the lead's score and the contact's seniority.
5. **Tracks the whole pipeline** on a drag-and-drop Kanban board: New → Enriched → Scored → Contacted → Replied → Won / Lost.

---

## Features

- **Offline-first** — 8 bundled mock company pages mean you can run the full pipeline without a single external request
- **Explainable scoring** — each lead gets a 0–100 score with a breakdown by industry fit, company size, contact seniority, tech stack overlap, and geography
- **Template-driven outreach** — four Jinja2 email templates, selected by score band and persona; no magic, just merge fields
- **React Kanban board** — drag leads between stages; the API updates instantly
- **Full lead lifecycle** — from raw scrape to won/lost, every transition is tracked
- **PostgreSQL + Alembic** — proper relational storage with versioned migrations

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn |
| Database | PostgreSQL 16, SQLAlchemy 2, Alembic |
| Scraping | httpx, selectolax |
| Templating | Jinja2 |
| Validation | Pydantic v2 |
| Frontend | React 18, TypeScript, Vite |
| Drag-and-drop | @hello-pangea/dnd |
| Container | Docker, docker-compose |
| Tests | pytest |

---

## Quick start

### Prerequisites
- Docker + Docker Compose (that's it)

### Run it

```bash
git clone https://github.com/omprxkash/ai-lead-generation.git
cd ai-lead-generation
docker compose up
```

The API will be at `http://localhost:8000`, the Kanban board at `http://localhost:5173`.

### Populate with mock leads

```bash
curl -X POST http://localhost:8000/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"mock": true}'
```

This scrapes all eight bundled company pages, enriches and scores them, drafts outreach emails, and saves everything to Postgres. Refresh the Kanban board and you'll see the leads appear with their scores.

### Run against real URLs

```bash
curl -X POST http://localhost:8000/pipeline/run \
  -H "Content-Type: application/json" \
  -d '{"mock": false, "urls": ["https://example.com", "https://another.io"]}'
```

---

## How it works

```mermaid
flowchart LR
    A[Company pages\nmock or live] --> B[Scraper\nselectolax]
    B --> C[Enricher\nnormalise + derive]
    C --> D[ICP Scorer\nweighted rules]
    D --> E[Email Generator\nJinja2 templates]
    E --> F[(PostgreSQL)]
    F --> G[Kanban Board\nReact]
```

### Scoring weights

The ICP config lives in `backend/data/icp_config.yaml` and is fully editable:

```yaml
weights:
  industry_match: 30   # Is the company in your target verticals?
  size_fit:       25   # Is headcount in the sweet spot (50–1000)?
  seniority:      20   # Is the contact a decision-maker?
  tech_match:     15   # Does their stack overlap with yours?
  geo_fit:        10   # Are they in a region you serve?

ideal:
  industries: [saas, fintech, devtools, data, cloud]
  size_min: 50
  size_max: 1000
  seniorities: [founder, ceo, cto, vp, head, director, chief]
  tech: [python, postgres, aws, react, fastapi, kubernetes, docker]
  regions: [US, EU, UK, CA]
```

Change any of these and the next pipeline run uses the new weights automatically.

---

## Project structure

```
ai-lead-generation/
├── backend/
│   ├── main.py                        # FastAPI app entry point
│   ├── db.py                          # SQLAlchemy engine + session
│   ├── pipeline/
│   │   ├── scraper.py                 # Fetch + parse company pages
│   │   ├── enricher.py                # Normalise and derive fields
│   │   ├── icp_scorer.py              # Weighted rule-based scoring
│   │   └── email_generator.py         # Jinja2 template selection + rendering
│   ├── routers/
│   │   ├── leads.py                   # GET /leads, PATCH /leads/{id}/stage
│   │   ├── pipeline.py                # POST /pipeline/run
│   │   └── templates.py               # GET/POST /templates
│   ├── models/
│   │   ├── db_models.py               # SQLAlchemy ORM models
│   │   └── schemas.py                 # Pydantic request/response schemas
│   ├── data/
│   │   ├── mock_sites/                # 8 bundled fake company pages
│   │   ├── icp_config.yaml            # Scoring weights and ideal profile
│   │   └── email_templates/           # Jinja2 .j2 email templates
│   ├── alembic/                       # Database migrations
│   ├── tests/
│   │   ├── test_scorer.py
│   │   ├── test_email.py
│   │   └── test_pipeline.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── App.tsx
│       ├── api/client.ts
│       └── components/
│           ├── KanbanBoard.tsx
│           ├── LeadCard.tsx
│           ├── LeadDrawer.tsx
│           └── ScoreBadge.tsx
├── docker-compose.yml
└── README.md
```

---

## API reference

| Method | Path | Description |
|---|---|---|
| `POST` | `/pipeline/run` | Run the full pipeline (mock or URL list) |
| `GET` | `/leads` | List leads; filter by `stage` and `min_score` |
| `GET` | `/leads/{id}` | Full lead detail with score breakdown and email draft |
| `PATCH` | `/leads/{id}/stage` | Move a lead to a new stage |
| `GET` | `/templates` | List saved email templates |
| `POST` | `/templates` | Create a new template |
| `GET` | `/health` | Health check |

The interactive API docs are at `http://localhost:8000/docs` when the server is running.

---

## Testing

The test suite runs against the real pipeline modules — no mocking of the core logic:

```bash
cd backend
pip install -r requirements.txt
pytest tests/ -v
```

What's covered:
- Every scoring factor in isolation (industry, size, seniority, tech, geo)
- Edge cases: zero tech overlap, enterprise-size companies, unknown seniority
- Email template rendering for every score band and industry category
- End-to-end mock pipeline: scrape → enrich → score → draft

---

## Configuration

Copy `.env.example` to `.env` in the `backend/` folder and adjust:

```
DATABASE_URL=postgresql://leaduser:leadpass@localhost:5432/leads
SENDER_NAME=Om
PORT=8000
```

`SENDER_NAME` is used in the outreach email sign-off. Everything else can stay as-is for local development.

---

## Known limitations

- **Mock data only** — the scraper is wired for the eight bundled HTML pages. Pointing it at real company sites will work for simple page structures, but most real sites need custom extraction logic.
- **Template emails, not generated ones** — outreach drafts are merge-field templates, not dynamically written. They're a good starting point, not a finished email.
- **No auth** — the API has no authentication layer. Don't expose it publicly as-is.
- **Single-user** — there's no concept of teams, roles, or multi-user ownership of leads.

---

## Contributing

Pull requests are welcome. For significant changes, open an issue first to talk through what you have in mind.

---

## License

MIT — see [LICENSE](LICENSE).

---

*Built by [Om Prakash](https://github.com/omprxkash)*


