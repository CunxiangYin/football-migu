"""Statistics model."""

from sqlalchemy import Column, String, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.domain.models.base import BaseModel


class Statistics(BaseModel):
    """Match statistics model."""
    
    __tablename__ = "statistics"
    
    # Foreign keys
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    
    # Indicator if these are home or away team stats
    is_home = Column(Boolean, nullable=False)
    
    # Possession and passing
    possession = Column(Float)
    passes = Column(Integer)
    passes_accurate = Column(Integer)
    pass_accuracy = Column(Float)
    
    # Shooting
    shots = Column(Integer)
    shots_on_target = Column(Integer)
    shots_off_target = Column(Integer)
    shots_blocked = Column(Integer)
    shots_inside_box = Column(Integer)
    shots_outside_box = Column(Integer)
    
    # Set pieces
    corners = Column(Integer)
    offsides = Column(Integer)
    free_kicks = Column(Integer)
    
    # Defensive
    fouls = Column(Integer)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    tackles = Column(Integer)
    interceptions = Column(Integer)
    saves = Column(Integer)
    
    # Advanced stats
    expected_goals = Column(Float)  # xG
    expected_goals_against = Column(Float)  # xGA
    touches_in_box = Column(Integer)
    dangerous_attacks = Column(Integer)
    
    # Season statistics (aggregated)
    season_goals_scored = Column(Integer)
    season_goals_conceded = Column(Integer)
    season_clean_sheets = Column(Integer)
    season_avg_goals_scored = Column(Float)
    season_avg_goals_conceded = Column(Float)
    
    # Form statistics (last 5 games)
    form_goals_scored = Column(Integer)
    form_goals_conceded = Column(Integer)
    form_avg_possession = Column(Float)
    form_avg_shots = Column(Float)
    
    # Relationships
    match = relationship("Match", back_populates="statistics")
    team = relationship("Team")
    
    def __repr__(self):
        return f"<Statistics for {self.team_id} in match {self.match_id}>"