from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db import get_db
from models.db_models import Lead
from models.schemas import LeadOut, StageUpdate

router = APIRouter(prefix="/leads", tags=["leads"])

VALID_STAGES = {"new", "enriched", "scored", "contacted", "replied", "won", "lost"}


@router.get("", response_model=list[LeadOut])
def list_leads(
    stage: str | None = Query(default=None),
    min_score: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    q = db.query(Lead)
    if stage:
        q = q.filter(Lead.stage == stage)
    if min_score is not None:
        q = q.filter(Lead.score >= min_score)
    return q.order_by(Lead.score.desc().nullslast()).all()


@router.get("/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: UUID, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}/stage", response_model=LeadOut)
def update_stage(lead_id: UUID, body: StageUpdate, db: Session = Depends(get_db)):
    if body.stage not in VALID_STAGES:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid stage. Must be one of: {sorted(VALID_STAGES)}",
        )
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead.stage = body.stage
    db.commit()
    db.refresh(lead)
    return lead

