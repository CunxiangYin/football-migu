"""Analysis model."""

from sqlalchemy import Column, String, Text, ForeignKey, JSON, Float, Integer
from sqlalchemy.orm import relationship

from app.domain.models.base import BaseModel


class Analysis(BaseModel):
    """Match analysis model."""
    
    __tablename__ = "analysis"
    
    # Foreign key
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False, unique=True)
    
    # Tactical analysis
    tactical_analysis = Column(Text)
    formation_home = Column(String(20))  # e.g., "4-3-3"
    formation_away = Column(String(20))
    
    # Key players
    key_players_home = Column(JSON, default=list)  # List of player objects
    key_players_away = Column(JSON, default=list)
    
    # Injury and suspension report
    injuries_home = Column(JSON, default=list)
    injuries_away = Column(JSON, default=list)
    suspensions_home = Column(JSON, default=list)
    suspensions_away = Column(JSON, default=list)
    
    # Form analysis
    home_form_last_5 = Column(String(5))  # e.g., "WWDLW"
    away_form_last_5 = Column(String(5))
    home_form_home = Column(String(5))  # Home team's form at home
    away_form_away = Column(String(5))  # Away team's form away
    
    # Head to head
    h2h_last_meetings = Column(JSON, default=list)  # List of recent meetings
    h2h_home_wins = Column(Integer, default=0)
    h2h_draws = Column(Integer, default=0)
    h2h_away_wins = Column(Integer, default=0)
    h2h_avg_goals = Column(Float, default=0.0)
    
    # Statistical edge
    statistical_edge = Column(Text)
    predicted_goals_home = Column(Float)
    predicted_goals_away = Column(Float)
    
    # Sentiment and importance
    sentiment_score = Column(Float)  # -1 to 1 (negative to positive)
    match_importance_home = Column(Integer, default=1)  # 1-5 scale
    match_importance_away = Column(Integer, default=1)
    
    # Additional insights
    weather_impact = Column(Text)
    referee_stats = Column(JSON)  # Referee tendencies
    venue_advantage = Column(Float)  # Home advantage factor
    
    # Relationship
    match = relationship("Match", back_populates="analysis")
    
    def __repr__(self):
        return f"<Analysis for match {self.match_id}>"