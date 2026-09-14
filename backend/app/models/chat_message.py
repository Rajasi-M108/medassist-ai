"""
RAG chat history (phase 5) -- one row per Q&A turn on a specific report.

Scaffolded now alongside the other models so the schema is complete and
migrations don't need to be redone later; the /chat endpoints themselves
come in the RAG phase.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True, default=_uuid)
    report_id = Column(String, ForeignKey("reports.id"), nullable=False)
    patient_id = Column(String, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    grounded = Column(Boolean, default=True, nullable=False)  # False = "not found in this report" fallback
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
