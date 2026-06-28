import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    picture: Mapped[str | None] = mapped_column(String, nullable=True)
    google_id: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_setup_complete: Mapped[int] = mapped_column(Integer, default=0)
    job_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    main_goal: Mapped[str | None] = mapped_column(Text, nullable=True)
    work_hours: Mapped[str | None] = mapped_column(String(255), nullable=True)
    personalization: Mapped[str] = mapped_column(Text, default="Be helpful, clear, and concise.")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    conversations: Mapped[list["Conversation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    memory_facts: Mapped[list["MemoryFact"]] = relationship(back_populates="user", cascade="all, delete-orphan")
