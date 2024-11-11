from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models.db_models import EmailTemplate
from models.schemas import TemplateBase, TemplateOut

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get("", response_model=list[TemplateOut])
def list_templates(db: Session = Depends(get_db)):
    return db.query(EmailTemplate).order_by(EmailTemplate.created_at.desc()).all()


@router.post("", response_model=TemplateOut, status_code=201)
def create_template(body: TemplateBase, db: Session = Depends(get_db)):
    existing = db.query(EmailTemplate).filter(EmailTemplate.name == body.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Template with this name already exists")
    template = EmailTemplate(name=body.name, subject=body.subject, body=body.body)
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

