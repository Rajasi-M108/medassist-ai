"""
Which doctor is responsible for which patient -- set by an Administrator.

A patient could in principle have more than one assigned doctor over
time (referrals, second opinions), so this is a join table rather than
a single `doctor_id` column on User; `is_active` marks the current
assignment without deleting history.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class PatientDoctorAssignment(Base):
    __tablename__ = "patient_doctor_assignments"

    id = Column(String, primary_key=True, default=_uuid)
    patient_id = Column(String, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(String, ForeignKey("users.id"), nullable=False)
    assigned_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True, nullable=False)

    patient = relationship("User", foreign_keys=[patient_id])
    doctor = relationship("User", foreign_keys=[doctor_id])
