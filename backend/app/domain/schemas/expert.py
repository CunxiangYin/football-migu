"""Expert schemas."""

from typing import Optional, List
from pydantic import Field
from datetime import datetime

from app.domain.schemas.common import BaseSchema


class Badge(BaseSchema):
    """Badge schema."""
    
    name: str
    icon: str
    color: str
    description: Optional[str] = None


class Performance(BaseSchema):
    """Recent performance schema."""
    
    date: datetime
    result: str  # "win", "loss", "push"
    profit: float
    odds: float


class ExpertBase(BaseSchema):
    """Expert base schema."""
    
    name: str = Field(..., min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)


class ExpertCreate(ExpertBase):
    """Expert creation schema."""
    
    badges: Optional[List[Badge]] = []
    specializations: Optional[List[str]] = []


class ExpertUpdate(BaseSchema):
    """Expert update schema."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    badges: Optional[List[Badge]] = None
    specializations: Optional[List[str]] = None


class ExpertStats(BaseSchema):
    """Expert statistics schema."""
    
    win_rate: float = Field(..., ge=0, le=100)
    avg_return: float
    total_predictions: int = Field(..., ge=0)
    successful_predictions: int = Field(..., ge=0)
    followers_count: int = Field(..., ge=0)
    recent_form: List[Performance] = []


class ExpertResponse(ExpertBase):
    """Expert response schema."""
    
    id: str
    win_rate: float
    avg_return: float
    total_predictions: int
    successful_predictions: int
    followers_count: int
    following_count: int
    badges: List[Badge]
    specializations: List[str]
    recent_form: List[Performance]
    created_at: datetime
    updated_at: datetime