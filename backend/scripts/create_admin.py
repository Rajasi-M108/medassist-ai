"""
Bootstrap the very first Administrator account.

Nobody can self-register as admin (see app/api/routes/auth.py), and
only an admin can create other admin/doctor accounts -- so this
command-line script exists purely to break that chicken-and-egg
problem once, right after the database is first created.

Usage (from the backend/ folder, with the venv active):
    python -m scripts.create_admin admin@medassist.local "Admin Name" SomeStrongPassword123
"""
import sys

sys.path.insert(0, ".")

from app.db.base import SessionLocal, Base, engine  # noqa: E402
from app import models  # noqa: E402, F401
from app.core.security import hash_password  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402


def main():
    if len(sys.argv) != 4:
        print("Usage: python -m scripts.create_admin <email> <full name> <password>")
        sys.exit(1)

    email, full_name, password = sys.argv[1], sys.argv[2], sys.argv[3]
    if len(password) < 8:
        print("Password must be at least 8 characters.")
        sys.exit(1)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            print(f"A user with email {email} already exists.")
            sys.exit(1)

        admin = User(
            email=email,
            hashed_password=hash_password(password),
            full_name=full_name,
            role=UserRole.admin,
        )
        db.add(admin)
        db.commit()
        print(f"Admin account created: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
