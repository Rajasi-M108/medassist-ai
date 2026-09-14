"""
Importing every model here means a single `from app import models` (or
importing this package) registers all tables on Base.metadata -- so
Base.metadata.create_all() in main.py actually creates all of them.
"""
from app.models.user import User, UserRole  # noqa: F401
from app.models.assignment import PatientDoctorAssignment  # noqa: F401
from app.models.report import Report, ReportType, ReportStatus  # noqa: F401
from app.models.clinical_note import ClinicalNote  # noqa: F401
from app.models.chat_message import ChatMessage  # noqa: F401
