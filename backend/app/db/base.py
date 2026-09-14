"""
SQLAlchemy engine/session wiring.

`get_db` is a FastAPI dependency: each request gets its own Session and
the session is always closed afterwards, even if the endpoint raises.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# SQLite needs this connect_arg because, by default, a SQLite connection
# may only be used by the thread that created it -- FastAPI can hand a
# request to a different thread than the one that opened the session.
# Postgres doesn't need (or accept) this argument.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
