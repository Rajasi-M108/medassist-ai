"""
An uploaded medical report (PDF lab/diagnostic report, or an X-ray image
stored for record-keeping only -- no AI analysis on images per spec).

`status` tracks the AI pipeline so the UI always has something honest
to show: uploaded -> processing -> analyzed, or analysis_unavailable
if text extraction fails (e.g. a scanned image PDF) -- the report is
still stored/downloadable even when analysis isn't possible.
"""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, ForeignKey, DateTime, Enum, Text, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class ReportType(str, enum.Enum):
    cbc = "cbc"
    urinalysis = "urinalysis"
    lipid_profile = "lipid_profile"
    metabolic_panel = "metabolic_panel"
    radiology = "radiology"
    xray_image = "xray_image"
    other = "other"


class ReportStatus(str, enum.Enum):
    uploaded = "uploaded"
    processing = "processing"
    analyzed = "analyzed"
    analysis_unavailable = "analysis_unavailable"


class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=_uuid)
    patient_id = Column(String, ForeignKey("users.id"), nullable=False)

    original_filename = Column(String, nullable=False)
    stored_path = Column(String, nullable=False)
    report_type = Column(Enum(ReportType), nullable=False, default=ReportType.other)
    status = Column(Enum(ReportStatus), nullable=False, default=ReportStatus.uploaded)

    # Populated by the AI pipeline (phase 4) -- plain strings/JSON so the
    # API can return them straight to the frontend with no extra joins.
    extracted_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    findings = Column(JSON, nullable=True)  # flagged out-of-range values + plain-language notes
    term_explanations = Column(JSON, nullable=True)

    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    analyzed_at = Column(DateTime, nullable=True)

    patient = relationship("User", back_populates="reports", foreign_keys=[patient_id])
    clinical_notes = relationship("ClinicalNote", back_populates="report")
