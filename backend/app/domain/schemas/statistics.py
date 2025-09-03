"""Statistics schemas."""

from typing import Optional
from pydantic import Field
from datetime import datetime

from app.domain.schemas.common import BaseSchema


class StatisticsBase(BaseSchema):
    """Statistics base schema."""
    
    # Possession and passing
    possession: Optional[float] = Field(None, ge=0, le=100)
    passes: Optional[int] = Field(None, ge=0)
    passes_accurate: Optional[int] = Field(None, ge=0)
    pass_accuracy: Optional[float] = Field(None, ge=0, le=100)
    
    # Shooting
    shots: Optional[int] = Field(None, ge=0)
    shots_on_target: Optional[int] = Field(None, ge=0)
    shots_off_target: Optional[int] = Field(None, ge=0)
    shots_blocked: Optional[int] = Field(None, ge=0)
    shots_inside_box: Optional[int] = Field(None, ge=0)
    shots_outside_box: Optional[int] = Field(None, ge=0)
    
    # Set pieces
    corners: Optional[int] = Field(None, ge=0)
    offsides: Optional[int] = Field(None, ge=0)
    free_kicks: Optional[int] = Field(None, ge=0)
    
    # Defensive
    fouls: Optional[int] = Field(None, ge=0)
    yellow_cards: Optional[int] = Field(None, ge=0)
    red_cards: Optional[int] = Field(None, ge=0)
    tackles: Optional[int] = Field(None, ge=0)
    interceptions: Optional[int] = Field(None, ge=0)
    saves: Optional[int] = Field(None, ge=0)
    
    # Advanced stats
    expected_goals: Optional[float] = Field(None, ge=0)
    expected_goals_against: Optional[float] = Field(None, ge=0)
    touches_in_box: Optional[int] = Field(None, ge=0)
    dangerous_attacks: Optional[int] = Field(None, ge=0)


class StatisticsCreate(StatisticsBase):
    """Statistics creation schema."""
    
    match_id: str
    team_id: str
    is_home: bool
    
    # Season statistics
    season_goals_scored: Optional[int] = Field(None, ge=0)
    season_goals_conceded: Optional[int] = Field(None, ge=0)
    season_clean_sheets: Optional[int] = Field(None, ge=0)
    season_avg_goals_scored: Optional[float] = Field(None, ge=0)
    season_avg_goals_conceded: Optional[float] = Field(None, ge=0)
    
    # Form statistics
    form_goals_scored: Optional[int] = Field(None, ge=0)
    form_goals_conceded: Optional[int] = Field(None, ge=0)
    form_avg_possession: Optional[float] = Field(None, ge=0, le=100)
    form_avg_shots: Optional[float] = Field(None, ge=0)


class StatisticsResponse(StatisticsBase):
    """Statistics response schema."""
    
    id: str
    match_id: str
    team_id: str
    team_name: Optional[str] = None
    is_home: bool
    
    # Season statistics
    season_goals_scored: Optional[int] = None
    season_goals_conceded: Optional[int] = None
    season_clean_sheets: Optional[int] = None
    season_avg_goals_scored: Optional[float] = None
    season_avg_goals_conceded: Optional[float] = None
    
    # Form statistics
    form_goals_scored: Optional[int] = None
    form_goals_conceded: Optional[int] = None
    form_avg_possession: Optional[float] = None
    form_avg_shots: Optional[float] = None
    
    created_at: datetime
    updated_at: datetime