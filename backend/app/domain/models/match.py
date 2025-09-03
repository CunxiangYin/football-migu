"""Match and Team models."""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.domain.models.base import BaseModel


class Team(BaseModel):
    """Team model."""
    
    __tablename__ = "teams"
    
    name = Column(String(100), nullable=False)
    code = Column(String(10))
    logo_url = Column(String(500))
    country = Column(String(100))
    founded_year = Column(Integer)
    stadium = Column(String(200))
    
    # Statistics
    league_position = Column(Integer)
    recent_form = Column(String(10))  # e.g., "WWDLW"
    
    # Relationships
    home_matches = relationship("Match", foreign_keys="Match.home_team_id", back_populates="home_team")
    away_matches = relationship("Match", foreign_keys="Match.away_team_id", back_populates="away_team")
    
    def __repr__(self):
        return f"<Team {self.name}>"


class Match(BaseModel):
    """Match model."""
    
    __tablename__ = "matches"
    
    # Teams
    home_team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    
    # Match information
    league = Column(String(100), nullable=False)
    match_date = Column(DateTime, nullable=False)
    status = Column(String(50), default="scheduled")  # scheduled, live, finished, postponed
    venue = Column(String(200))
    referee = Column(String(100))
    attendance = Column(Integer)
    
    # Score (if finished)
    home_score = Column(Integer)
    away_score = Column(Integer)
    
    # Additional information
    round = Column(String(50))
    season = Column(String(20))
    importance_level = Column(Integer, default=1)  # 1-5 scale
    weather = Column(String(50))
    
    # Relationships
    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    predictions = relationship("Prediction", back_populates="match", cascade="all, delete-orphan")
    betting_odds = relationship("BettingOdds", back_populates="match", cascade="all, delete-orphan")
    analysis = relationship("Analysis", back_populates="match", uselist=False, cascade="all, delete-orphan")
    statistics = relationship("Statistics", back_populates="match", cascade="all, delete-orphan")
    engagement = relationship("Engagement", back_populates="match", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Match {self.home_team_id} vs {self.away_team_id}>"