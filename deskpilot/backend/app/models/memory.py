import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import VECTOR
from app.core.database import Base


class MemoryFact(Base):
    __tablename__ = "memory_facts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    category: Mapped[str] = mapped_column(String)  # preference | habit | project | contact
    content: Mapped[str] = mapped_column(Text)
    importance: Mapped[float] = mapped_column(Float, default=0.5)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="memory_facts")
    embedding: Mapped["MemoryEmbedding"] = relationship(back_populates="fact", cascade="all, delete-orphan", uselist=False)


class MemoryEmbedding(Base):
    __tablename__ = "memory_embeddings"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    fact_id: Mapped[str] = mapped_column(String, ForeignKey("memory_facts.id"))
    vector = mapped_column(VECTOR(768))

    fact: Mapped["MemoryFact"] = relationship(back_populates="embedding")
