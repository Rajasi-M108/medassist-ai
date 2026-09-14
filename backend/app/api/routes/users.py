"""
Administrator-only user management: create doctor/admin accounts,
activate/deactivate any account, and assign patients to doctors.

Every route here is gated by require_role(UserRole.admin) -- see
app/api/deps.py.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.core.security import hash_password
from app.db.base import get_db
from app.models.assignment import PatientDoctorAssignment
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/users", tags=["users (admin)"])


@router.get("", response_model=list[UserOut])
def list_users(
    role: UserRole | None = None,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
):
    query = db.query(User)
    if role is not None:
        query = query.filter(User.role == role)
    return query.order_by(User.created_at.desc()).all()


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
):
    """Admin-provisioned account -- this is the only way to create a
    doctor or another admin (see auth.register for why)."""
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}/active", response_model=UserOut)
def set_active(
    user_id: str,
    is_active: bool,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user


@router.post("/assign", status_code=status.HTTP_201_CREATED)
def assign_patient_to_doctor(
    patient_id: str,
    doctor_id: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role(UserRole.admin)),
):
    patient = db.query(User).filter(User.id == patient_id, User.role == UserRole.patient).first()
    doctor = db.query(User).filter(User.id == doctor_id, User.role == UserRole.doctor).first()
    if not patient or not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient or doctor not found")

    # Deactivate any previous active assignment for this patient before
    # creating the new one, so "current doctor" is always unambiguous.
    db.query(PatientDoctorAssignment).filter(
        PatientDoctorAssignment.patient_id == patient_id,
        PatientDoctorAssignment.is_active == True,  # noqa: E712
    ).update({"is_active": False})

    assignment = PatientDoctorAssignment(patient_id=patient_id, doctor_id=doctor_id)
    db.add(assignment)
    db.commit()
    return {"detail": f"{patient.full_name} assigned to Dr. {doctor.full_name}"}
