"""Expert model."""

from sqlalchemy import Column, String, Float, Integer, JSON
from sqlalchemy.orm import relationship

from app.domain.models.base import BaseModel


class Expert(BaseModel):
    """Expert model for betting predictions."""
    
    __tablename__ = "experts"
    
    # Basic information
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(500))
    bio = Column(String(500))
    
    # Statistics
    win_rate = Column(Float, default=0.0)
    avg_return = Column(Float, default=0.0)
    total_predictions = Column(Integer, default=0)
    successful_predictions = Column(Integer, default=0)
    
    # Social
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    
    # Additional data
    badges = Column(JSON, default=list)  # List of badge objects
    specializations = Column(JSON, default=list)  # List of leagues/teams
    recent_form = Column(JSON, default=list)  # Recent prediction results
    
    # Relationships
    predictions = relationship("Prediction", back_populates="expert", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Expert {self.name}>"