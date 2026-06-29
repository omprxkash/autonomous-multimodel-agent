import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, JSON, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum


class AnalysisType(str, enum.Enum):
    EMAIL = "email"
    URL = "url"


class Verdict(str, enum.Enum):
    SAFE = "SAFE"
    MARKETING = "MARKETING"
    SUSPICIOUS = "SUSPICIOUS"
    PHISHING = "PHISHING"


class AnalysisStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type: Mapped[AnalysisType] = mapped_column(SAEnum(AnalysisType))
    target: Mapped[str] = mapped_column(String)
    status: Mapped[AnalysisStatus] = mapped_column(SAEnum(AnalysisStatus), default=AnalysisStatus.PENDING)
    verdict: Mapped[str | None] = mapped_column(SAEnum(Verdict), nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    pipeline_results: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    feature_vector: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    iocs: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error: Mapped[str | None] = mapped_column(String, nullable=True)
