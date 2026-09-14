"""
User model shared by all three roles (Patient, Doctor, Administrator).

One table with a `role` column -- rather than separate Patient/Doctor
tables -- keeps auth simple (one login endpoint, one JWT shape) while
RBAC is enforced in app/api/deps.py by checking `role` on each
protected route.
"""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    patient = "patient"
    doctor = "doctor"
    admin = "admin"


def _uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.patient)

    # Admins can deactivate an account instead of deleting it, so history
    # (reports, notes) is preserved but the user can no longer log in.
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reports = relationship(
        "Report", back_populates="patient", foreign_keys="Report.patient_id"
    )
    clinical_notes_written = relationship(
        "ClinicalNote", back_populates="doctor", foreign_keys="ClinicalNote.doctor_id"
    )
