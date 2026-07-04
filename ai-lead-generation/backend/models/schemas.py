from __future__ import annotations
from datetime import datetime
from typing import Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class LeadBase(BaseModel):
    company: str
    domain: str
    industry: str | None = None
    employee_count: int | None = None
    location: str | None = None
    contact_name: str | None = None
    title: str | None = None
    email: str | None = None
    tech_stack: list[str] = Field(default_factory=list)


class LeadOut(LeadBase):
    id: UUID
    score: int | None = None
    score_breakdown: dict[str, Any] | None = None
    email_draft: str | None = None
    stage: str = "new"
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class StageUpdate(BaseModel):
    stage: str


class PipelineRunRequest(BaseModel):
    mock: bool = True
    urls: list[str] = Field(default_factory=list)
    use_llm: bool = False


class PipelineRunResponse(BaseModel):
    processed: int
    leads: list[LeadOut]


class TemplateBase(BaseModel):
    name: str
    subject: str
    body: str


class TemplateOut(TemplateBase):
    id: UUID
    created_at: datetime | None = None

    model_config = {"from_attributes": True}

