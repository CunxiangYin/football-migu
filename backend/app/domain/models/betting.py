"""Betting odds model."""

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.models.base import BaseModel


class BettingOdds(BaseModel):
    """Betting odds from various bookmakers."""
    
    __tablename__ = "betting_odds"
    
    # Foreign key
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    
    # Bookmaker
    bookmaker = Column(String(100), nullable=False)
    
    # Match result odds (1X2)
    home_win = Column(Float, nullable=False)
    draw = Column(Float, nullable=False)
    away_win = Column(Float, nullable=False)
    
    # Over/Under goals
    over_0_5 = Column(Float)
    under_0_5 = Column(Float)
    over_1_5 = Column(Float)
    under_1_5 = Column(Float)
    over_2_5 = Column(Float)
    under_2_5 = Column(Float)
    over_3_5 = Column(Float)
    under_3_5 = Column(Float)
    
    # Both teams to score
    btts_yes = Column(Float)
    btts_no = Column(Float)
    
    # Asian handicap
    handicap_home_line = Column(Float)
    handicap_home_odds = Column(Float)
    handicap_away_line = Column(Float)
    handicap_away_odds = Column(Float)
    
    # Double chance
    home_draw = Column(Float)
    home_away = Column(Float)
    draw_away = Column(Float)
    
    # Correct score (popular ones)
    score_0_0 = Column(Float)
    score_1_0 = Column(Float)
    score_2_0 = Column(Float)
    score_1_1 = Column(Float)
    score_2_1 = Column(Float)
    score_0_1 = Column(Float)
    score_0_2 = Column(Float)
    score_1_2 = Column(Float)
    
    # Relationship
    match = relationship("Match", back_populates="betting_odds")
    
    def __repr__(self):
        return f"<BettingOdds {self.bookmaker} for {self.match_id}>"