from datetime import datetime, timezone, timedelta
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db import get_db
from models.db_models import Lead, FollowUp

router = APIRouter(prefix="/followups", tags=["followups"])


class ScheduleFollowUpRequest(BaseModel):
    lead_id: UUID
    sequence_step: int = 1
    delay_days: int = 3
    subject: str
    body: str


class FollowUpOut(BaseModel):
    id: UUID
    lead_id: UUID
    sequence_step: int
    scheduled_at: datetime
    sent_at: datetime | None
    status: str
    subject: str
    body: str

    class Config:
        from_attributes = True


@router.post("", response_model=FollowUpOut)
def schedule_follow_up(req: ScheduleFollowUpRequest, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == req.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    scheduled = datetime.now(timezone.utc) + timedelta(days=req.delay_days)
    fu = FollowUp(
        lead_id=req.lead_id,
        sequence_step=req.sequence_step,
        scheduled_at=scheduled,
        subject=req.subject,
        body=req.body,
    )
    db.add(fu)
    db.commit()
    db.refresh(fu)
    return fu


@router.get("", response_model=list[FollowUpOut])
def list_follow_ups(
    lead_id: UUID | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(FollowUp)
    if lead_id:
        q = q.filter(FollowUp.lead_id == lead_id)
    if status:
        q = q.filter(FollowUp.status == status)
    return q.order_by(FollowUp.scheduled_at).all()


@router.patch("/{followup_id}/send", response_model=FollowUpOut)
def mark_sent(followup_id: UUID, db: Session = Depends(get_db)):
    fu = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not fu:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    fu.status = "sent"
    fu.sent_at = datetime.now(timezone.utc)
    fu.lead.stage = "contacted"
    db.commit()
    db.refresh(fu)
    return fu


@router.patch("/{followup_id}/skip", response_model=FollowUpOut)
def skip_follow_up(followup_id: UUID, db: Session = Depends(get_db)):
    fu = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if not fu:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    fu.status = "skipped"
    db.commit()
    db.refresh(fu)
    return fu
