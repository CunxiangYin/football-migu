"""Prediction model."""

from sqlalchemy import Column, String, Float, ForeignKey, Text, Boolean, Integer
from sqlalchemy.orm import relationship

from app.domain.models.base import BaseModel


class Prediction(BaseModel):
    """Prediction model for match outcomes."""
    
    __tablename__ = "predictions"
    
    # Foreign keys
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False)
    expert_id = Column(String(36), ForeignKey("experts.id"), nullable=False)
    
    # Prediction details
    prediction_type = Column(String(50), nullable=False)  # match_result, over_under, btts, etc.
    predicted_outcome = Column(String(100), nullable=False)  # home_win, draw, away_win, over_2.5, etc.
    confidence = Column(Float, nullable=False)  # 0-100
    stake_level = Column(String(20))  # low, medium, high
    
    # Odds and potential return
    odds = Column(Float)
    potential_return = Column(Float)
    
    # Reasoning
    reasoning = Column(Text)
    key_factors = Column(Text)  # JSON string of factors
    
    # Result (after match)
    is_correct = Column(Boolean)
    actual_return = Column(Float)
    
    # Engagement
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    # Relationships
    match = relationship("Match", back_populates="predictions")
    expert = relationship("Expert", back_populates="predictions")
    
    def __repr__(self):
        return f"<Prediction {self.expert_id} for {self.match_id}>"