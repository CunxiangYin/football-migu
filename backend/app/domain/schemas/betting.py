"""Betting odds schemas."""

from typing import Optional
from pydantic import Field
from datetime import datetime

from app.domain.schemas.common import BaseSchema


class BettingOddsBase(BaseSchema):
    """Betting odds base schema."""
    
    bookmaker: str = Field(..., min_length=1, max_length=100)
    home_win: float = Field(..., gt=1.0)
    draw: float = Field(..., gt=1.0)
    away_win: float = Field(..., gt=1.0)


class BettingOddsCreate(BettingOddsBase):
    """Betting odds creation schema."""
    
    match_id: str
    # Over/Under
    over_0_5: Optional[float] = Field(None, gt=1.0)
    under_0_5: Optional[float] = Field(None, gt=1.0)
    over_1_5: Optional[float] = Field(None, gt=1.0)
    under_1_5: Optional[float] = Field(None, gt=1.0)
    over_2_5: Optional[float] = Field(None, gt=1.0)
    under_2_5: Optional[float] = Field(None, gt=1.0)
    over_3_5: Optional[float] = Field(None, gt=1.0)
    under_3_5: Optional[float] = Field(None, gt=1.0)
    
    # Both teams to score
    btts_yes: Optional[float] = Field(None, gt=1.0)
    btts_no: Optional[float] = Field(None, gt=1.0)
    
    # Asian handicap
    handicap_home_line: Optional[float] = None
    handicap_home_odds: Optional[float] = Field(None, gt=1.0)
    handicap_away_line: Optional[float] = None
    handicap_away_odds: Optional[float] = Field(None, gt=1.0)
    
    # Double chance
    home_draw: Optional[float] = Field(None, gt=1.0)
    home_away: Optional[float] = Field(None, gt=1.0)
    draw_away: Optional[float] = Field(None, gt=1.0)
    
    # Correct score
    score_0_0: Optional[float] = Field(None, gt=1.0)
    score_1_0: Optional[float] = Field(None, gt=1.0)
    score_2_0: Optional[float] = Field(None, gt=1.0)
    score_1_1: Optional[float] = Field(None, gt=1.0)
    score_2_1: Optional[float] = Field(None, gt=1.0)
    score_0_1: Optional[float] = Field(None, gt=1.0)
    score_0_2: Optional[float] = Field(None, gt=1.0)
    score_1_2: Optional[float] = Field(None, gt=1.0)


class BettingOddsResponse(BettingOddsBase):
    """Betting odds response schema."""
    
    id: str
    match_id: str
    
    # Over/Under
    over_0_5: Optional[float] = None
    under_0_5: Optional[float] = None
    over_1_5: Optional[float] = None
    under_1_5: Optional[float] = None
    over_2_5: Optional[float] = None
    under_2_5: Optional[float] = None
    over_3_5: Optional[float] = None
    under_3_5: Optional[float] = None
    
    # Both teams to score
    btts_yes: Optional[float] = None
    btts_no: Optional[float] = None
    
    # Asian handicap
    handicap_home_line: Optional[float] = None
    handicap_home_odds: Optional[float] = None
    handicap_away_line: Optional[float] = None
    handicap_away_odds: Optional[float] = None
    
    # Double chance
    home_draw: Optional[float] = None
    home_away: Optional[float] = None
    draw_away: Optional[float] = None
    
    # Correct score (selected)
    score_0_0: Optional[float] = None
    score_1_0: Optional[float] = None
    score_2_0: Optional[float] = None
    score_1_1: Optional[float] = None
    score_2_1: Optional[float] = None
    score_0_1: Optional[float] = None
    score_0_2: Optional[float] = None
    score_1_2: Optional[float] = None
    
    created_at: datetime
    updated_at: datetime