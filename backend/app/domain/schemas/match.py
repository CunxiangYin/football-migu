"""Match schemas."""

from typing import Optional, List
from pydantic import Field
from datetime import datetime
from enum import Enum

from app.domain.schemas.common import BaseSchema


class MatchStatus(str, Enum):
    """Match status enumeration."""
    
    SCHEDULED = "scheduled"
    LIVE = "live"
    FINISHED = "finished"
    POSTPONED = "postponed"
    CANCELLED = "cancelled"


class TeamBase(BaseSchema):
    """Team base schema."""
    
    name: str = Field(..., min_length=1, max_length=100)
    code: Optional[str] = Field(None, max_length=10)
    logo_url: Optional[str] = None
    country: Optional[str] = Field(None, max_length=100)


class TeamCreate(TeamBase):
    """Team creation schema."""
    
    founded_year: Optional[int] = None
    stadium: Optional[str] = Field(None, max_length=200)


class TeamResponse(TeamBase):
    """Team response schema."""
    
    id: str
    founded_year: Optional[int] = None
    stadium: Optional[str] = None
    league_position: Optional[int] = None
    recent_form: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class MatchBase(BaseSchema):
    """Match base schema."""
    
    league: str = Field(..., min_length=1, max_length=100)
    match_date: datetime
    venue: Optional[str] = Field(None, max_length=200)
    referee: Optional[str] = Field(None, max_length=100)


class MatchCreate(MatchBase):
    """Match creation schema."""
    
    home_team_id: str
    away_team_id: str
    status: MatchStatus = MatchStatus.SCHEDULED
    round: Optional[str] = Field(None, max_length=50)
    season: Optional[str] = Field(None, max_length=20)
    importance_level: int = Field(default=1, ge=1, le=5)


class MatchUpdate(BaseSchema):
    """Match update schema."""
    
    status: Optional[MatchStatus] = None
    home_score: Optional[int] = Field(None, ge=0)
    away_score: Optional[int] = Field(None, ge=0)
    attendance: Optional[int] = Field(None, ge=0)
    weather: Optional[str] = Field(None, max_length=50)


class MatchResponse(MatchBase):
    """Match response schema."""
    
    id: str
    home_team: TeamResponse
    away_team: TeamResponse
    status: MatchStatus
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    round: Optional[str] = None
    season: Optional[str] = None
    importance_level: int
    weather: Optional[str] = None
    attendance: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class MatchListItem(BaseSchema):
    """Match list item for listing endpoints."""
    
    id: str
    home_team: TeamResponse
    away_team: TeamResponse
    league: str
    match_date: datetime
    status: MatchStatus
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    predictions_count: int = 0
    trending_score: float = 0.0


class MatchDetail(MatchResponse):
    """Detailed match response with all related data."""
    
    predictions: Optional[List] = []  # Will be PredictionResponse
    betting_odds: Optional[List] = []  # Will be BettingOddsResponse
    analysis: Optional[dict] = None  # Will be AnalysisResponse
    statistics: Optional[List] = []  # Will be StatisticsResponse
    engagement: Optional[dict] = None  # Will be EngagementResponse