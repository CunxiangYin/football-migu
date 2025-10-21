"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# Create engine
engine = create_engine(
    settings.get_database_url(),
    connect_args={"check_same_thread": False} if settings.get_database_url().startswith("sqlite") else {},
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database tables."""
    import os
    from pathlib import Path
    
    # Ensure data directory exists for SQLite
    db_url = settings.get_database_url()
    if db_url.startswith("sqlite"):
        # Extract path from SQLite URL
        db_path = db_url.replace("sqlite:///", "")
        if db_path and db_path != ":memory:":
            # Create parent directory if it doesn't exist
            db_dir = os.path.dirname(db_path)
            if db_dir:
                Path(db_dir).mkdir(parents=True, exist_ok=True)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)