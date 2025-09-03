"""Engagement model."""

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.domain.models.base import BaseModel


class Engagement(BaseModel):
    """User engagement metrics for matches."""
    
    __tablename__ = "engagement"
    
    # Foreign key
    match_id = Column(String(36), ForeignKey("matches.id"), nullable=False, unique=True)
    
    # Engagement metrics
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    bookmarks = Column(Integer, default=0)
    
    # Tips and rewards
    tips_count = Column(Integer, default=0)
    tips_amount = Column(Float, default=0.0)
    
    # Activity tracking
    unique_visitors = Column(Integer, default=0)
    avg_time_spent = Column(Float, default=0.0)  # in seconds
    bounce_rate = Column(Float, default=0.0)  # percentage
    
    # Trending score
    trending_score = Column(Float, default=0.0)  # Calculated based on recent activity
    
    # Relationship
    match = relationship("Match", back_populates="engagement")
    
    def __repr__(self):
        return f"<Engagement for match {self.match_id}>"