"""Analysis schemas."""

from typing import Optional, List, Dict, Any
from pydantic import Field
from datetime import datetime

from app.domain.schemas.common import BaseSchema


class Player(BaseSchema):
    """Player schema."""
    
    name: str
    position: str
    number: Optional[int] = None
    status: str  # fit, doubtful, injured
    importance: int = Field(default=1, ge=1, le=5)


class InjuryReport(BaseSchema):
    """Injury report schema."""
    
    player_name: str
    injury_type: str
    expected_return: Optional[datetime] = None
    impact: str  # high, medium, low


class H2HMatch(BaseSchema):
    """Head to head match schema."""
    
    date: datetime
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    competition: str


class RefereeStats(BaseSchema):
    """Referee statistics schema."""
    
    avg_cards_per_game: float
    avg_fouls_per_game: float
    home_win_percentage: float
    strict_level: int = Field(default=3, ge=1, le=5)


class AnalysisBase(BaseSchema):
    """Analysis base schema."""
    
    tactical_analysis: Optional[str] = None
    formation_home: Optional[str] = Field(None, pattern=r"^\d-\d-\d$|^\d-\d-\d-\d$")
    formation_away: Optional[str] = Field(None, pattern=r"^\d-\d-\d$|^\d-\d-\d-\d$")
    statistical_edge: Optional[str] = None
    weather_impact: Optional[str] = None


class AnalysisCreate(AnalysisBase):
    """Analysis creation schema."""
    
    match_id: str
    key_players_home: Optional[List[Player]] = []
    key_players_away: Optional[List[Player]] = []
    injuries_home: Optional[List[InjuryReport]] = []
    injuries_away: Optional[List[InjuryReport]] = []
    suspensions_home: Optional[List[Dict[str, Any]]] = []
    suspensions_away: Optional[List[Dict[str, Any]]] = []
    home_form_last_5: Optional[str] = Field(None, pattern=r"^[WDL]{5}$")
    away_form_last_5: Optional[str] = Field(None, pattern=r"^[WDL]{5}$")
    home_form_home: Optional[str] = Field(None, pattern=r"^[WDL]{5}$")
    away_form_away: Optional[str] = Field(None, pattern=r"^[WDL]{5}$")
    h2h_last_meetings: Optional[List[H2HMatch]] = []
    predicted_goals_home: Optional[float] = Field(None, ge=0)
    predicted_goals_away: Optional[float] = Field(None, ge=0)
    sentiment_score: Optional[float] = Field(None, ge=-1, le=1)
    match_importance_home: Optional[int] = Field(None, ge=1, le=5)
    match_importance_away: Optional[int] = Field(None, ge=1, le=5)
    referee_stats: Optional[RefereeStats] = None
    venue_advantage: Optional[float] = Field(None, ge=0, le=1)


class AnalysisResponse(AnalysisBase):
    """Analysis response schema."""
    
    id: str
    match_id: str
    key_players_home: List[Player]
    key_players_away: List[Player]
    injuries_home: List[InjuryReport]
    injuries_away: List[InjuryReport]
    suspensions_home: List[Dict[str, Any]]
    suspensions_away: List[Dict[str, Any]]
    home_form_last_5: Optional[str] = None
    away_form_last_5: Optional[str] = None
    home_form_home: Optional[str] = None
    away_form_away: Optional[str] = None
    h2h_last_meetings: List[H2HMatch]
    h2h_home_wins: int = 0
    h2h_draws: int = 0
    h2h_away_wins: int = 0
    h2h_avg_goals: float = 0.0
    predicted_goals_home: Optional[float] = None
    predicted_goals_away: Optional[float] = None
    sentiment_score: Optional[float] = None
    match_importance_home: int = 1
    match_importance_away: int = 1
    referee_stats: Optional[RefereeStats] = None
    venue_advantage: Optional[float] = None
    created_at: datetime
    updated_at: datetime