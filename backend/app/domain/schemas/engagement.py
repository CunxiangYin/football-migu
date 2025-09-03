"""Engagement schemas."""

from typing import Optional
from pydantic import Field
from datetime import datetime

from app.domain.schemas.common import BaseSchema


class EngagementBase(BaseSchema):
    """Engagement base schema."""
    
    views: int = Field(default=0, ge=0)
    likes: int = Field(default=0, ge=0)
    comments: int = Field(default=0, ge=0)
    shares: int = Field(default=0, ge=0)
    bookmarks: int = Field(default=0, ge=0)


class EngagementUpdate(BaseSchema):
    """Engagement update schema."""
    
    views: Optional[int] = Field(None, ge=0)
    likes: Optional[int] = Field(None, ge=0)
    comments: Optional[int] = Field(None, ge=0)
    shares: Optional[int] = Field(None, ge=0)
    bookmarks: Optional[int] = Field(None, ge=0)
    tips_count: Optional[int] = Field(None, ge=0)
    tips_amount: Optional[float] = Field(None, ge=0)


class EngagementResponse(EngagementBase):
    """Engagement response schema."""
    
    id: str
    match_id: str
    tips_count: int = 0
    tips_amount: float = 0.0
    unique_visitors: int = 0
    avg_time_spent: float = 0.0
    bounce_rate: float = 0.0
    trending_score: float = 0.0
    created_at: datetime
    updated_at: datetime


class LikeRequest(BaseSchema):
    """Like request schema."""
    
    user_id: Optional[str] = None  # For future user tracking


class FollowRequest(BaseSchema):
    """Follow request schema."""
    
    user_id: Optional[str] = None  # For future user tracking
    action: str = Field(..., pattern="^(follow|unfollow)$")