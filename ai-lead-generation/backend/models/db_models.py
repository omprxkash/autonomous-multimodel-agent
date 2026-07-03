import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from db import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company = Column(String, nullable=False)
    domain = Column(String, unique=True, nullable=False)
    industry = Column(String)
    employee_count = Column(Integer)
    location = Column(String)
    contact_name = Column(String)
    title = Column(String)
    email = Column(String)
    tech_stack = Column(JSONB, default=list)
    score = Column(Integer)
    score_breakdown = Column(JSONB)
    email_draft = Column(Text)
    stage = Column(String, default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
