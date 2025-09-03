"""Base model with common fields."""

from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.core.database import Base


class BaseModel(Base):
    """Abstract base model with common fields."""
    
    __abstract__ = True
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now(), nullable=False)