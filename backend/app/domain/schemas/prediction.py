"""Prediction schemas."""

from typing import Optional
from pydantic import Field
from datetime import datetime
from enum import Enum

from app.domain.schemas.common import BaseSchema
from app.domain.schemas.expert import ExpertResponse


class PredictionType(str, Enum):
    """Prediction type enumeration."""
    
    MATCH_RESULT = "match_result"
    OVER_UNDER = "over_under"
    BTTS = "btts"
    CORRECT_SCORE = "correct_score"
    ASIAN_HANDICAP = "asian_handicap"
    DOUBLE_CHANCE = "double_chance"
    FIRST_GOAL = "first_goal"


class StakeLevel(str, Enum):
    """Stake level enumeration."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PredictionBase(BaseSchema):
    """Prediction base schema."""
    
    prediction_type: PredictionType
    predicted_outcome: str = Field(..., min_length=1, max_length=100)
    confidence: float = Field(..., ge=0, le=100)
    stake_level: Optional[StakeLevel] = None
    reasoning: Optional[str] = None
    key_factors: Optional[str] = None


class PredictionCreate(PredictionBase):
    """Prediction creation schema."""
    
    match_id: str
    expert_id: str
    odds: Optional[float] = Field(None, gt=1.0)
    potential_return: Optional[float] = Field(None, gt=0)


class PredictionUpdate(BaseSchema):
    """Prediction update schema."""
    
    is_correct: Optional[bool] = None
    actual_return: Optional[float] = None


class PredictionResponse(PredictionBase):
    """Prediction response schema."""
    
    id: str
    match_id: str
    expert: ExpertResponse
    odds: Optional[float] = None
    potential_return: Optional[float] = None
    is_correct: Optional[bool] = None
    actual_return: Optional[float] = None
    likes_count: int = 0
    comments_count: int = 0
    created_at: datetime