from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.db_models import Lead
from models.schemas import PipelineRunRequest, PipelineRunResponse, LeadOut
from pipeline.scraper import scrape_mock, scrape_urls
from pipeline.enricher import enrich_all
from pipeline.icp_scorer import score_all
from pipeline.email_generator import generate

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("/run", response_model=PipelineRunResponse)
def run_pipeline(body: PipelineRunRequest, db: Session = Depends(get_db)):
    if body.mock:
        raws = scrape_mock()
    elif body.urls:
        raws = scrape_urls(body.urls)
    else:
        raise HTTPException(status_code=422, detail="Provide mock=true or a list of URLs")

    if not raws:
        raise HTTPException(status_code=422, detail="No leads scraped from provided sources")

    enriched = enrich_all(raws)
    scored_pairs = score_all(enriched)

    saved: list[Lead] = []
    for enriched_lead, result in scored_pairs:
        existing = db.query(Lead).filter(Lead.domain == enriched_lead.domain).first()
        if existing:
            existing.score = result["score"]
            existing.score_breakdown = result["breakdown"]
            existing.email_draft = generate(enriched_lead, result["score"])
            existing.stage = "scored"
            db.commit()
            db.refresh(existing)
            saved.append(existing)
            continue

        email_draft = generate(enriched_lead, result["score"])
        lead = Lead(
            company=enriched_lead.company,
            domain=enriched_lead.domain,
            industry=enriched_lead.industry,
            employee_count=enriched_lead.employee_count,
            location=enriched_lead.location,
            contact_name=enriched_lead.contact_name,
            title=enriched_lead.title,
            email=enriched_lead.email,
            tech_stack=enriched_lead.tech_stack,
            score=result["score"],
            score_breakdown=result["breakdown"],
            email_draft=email_draft,
            stage="scored",
        )
        db.add(lead)
        db.commit()
        db.refresh(lead)
        saved.append(lead)

    return PipelineRunResponse(
        processed=len(saved),
        leads=[LeadOut.model_validate(l) for l in saved],
    )

