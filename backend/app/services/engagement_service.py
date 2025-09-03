"""Engagement service."""

from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime

from app.domain.models import Engagement, Match


class EngagementService:
    """Service for engagement-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def like_match(self, match_id: str, user_id: Optional[str] = None) -> bool:
        """Like a match."""
        # Check if match exists
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            return False
        
        # Get or create engagement
        engagement = self.db.query(Engagement).filter(
            Engagement.match_id == match_id
        ).first()
        
        if not engagement:
            engagement = Engagement(
                match_id=match_id,
                likes=1,
                views=1
            )
            self.db.add(engagement)
        else:
            engagement.likes += 1
        
        # Update trending score (simple algorithm)
        self._update_trending_score(engagement)
        
        self.db.commit()
        return True
    
    def view_match(self, match_id: str, user_id: Optional[str] = None) -> bool:
        """Record a match view."""
        # Check if match exists
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            return False
        
        # Get or create engagement
        engagement = self.db.query(Engagement).filter(
            Engagement.match_id == match_id
        ).first()
        
        if not engagement:
            engagement = Engagement(
                match_id=match_id,
                views=1
            )
            self.db.add(engagement)
        else:
            engagement.views += 1
            if user_id:
                engagement.unique_visitors += 1
        
        # Update trending score
        self._update_trending_score(engagement)
        
        self.db.commit()
        return True
    
    def add_comment(self, match_id: str, user_id: Optional[str] = None) -> bool:
        """Add a comment to a match."""
        # Check if match exists
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            return False
        
        # Get or create engagement
        engagement = self.db.query(Engagement).filter(
            Engagement.match_id == match_id
        ).first()
        
        if not engagement:
            engagement = Engagement(
                match_id=match_id,
                comments=1,
                views=1
            )
            self.db.add(engagement)
        else:
            engagement.comments += 1
        
        # Update trending score
        self._update_trending_score(engagement)
        
        self.db.commit()
        return True
    
    def share_match(self, match_id: str, user_id: Optional[str] = None) -> bool:
        """Share a match."""
        # Check if match exists
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            return False
        
        # Get or create engagement
        engagement = self.db.query(Engagement).filter(
            Engagement.match_id == match_id
        ).first()
        
        if not engagement:
            engagement = Engagement(
                match_id=match_id,
                shares=1,
                views=1
            )
            self.db.add(engagement)
        else:
            engagement.shares += 1
        
        # Update trending score
        self._update_trending_score(engagement)
        
        self.db.commit()
        return True
    
    def tip_expert(self, match_id: str, amount: float, user_id: Optional[str] = None) -> bool:
        """Send a tip for a match prediction."""
        # Check if match exists
        match = self.db.query(Match).filter(Match.id == match_id).first()
        if not match:
            return False
        
        # Get or create engagement
        engagement = self.db.query(Engagement).filter(
            Engagement.match_id == match_id
        ).first()
        
        if not engagement:
            engagement = Engagement(
                match_id=match_id,
                tips_count=1,
                tips_amount=amount,
                views=1
            )
            self.db.add(engagement)
        else:
            engagement.tips_count += 1
            engagement.tips_amount += amount
        
        # Update trending score
        self._update_trending_score(engagement)
        
        self.db.commit()
        return True
    
    def _update_trending_score(self, engagement: Engagement):
        """Update trending score based on engagement metrics."""
        # Simple trending algorithm
        # Weight: views(1), likes(3), comments(5), shares(7), tips(10)
        score = (
            engagement.views * 1 +
            engagement.likes * 3 +
            engagement.comments * 5 +
            engagement.shares * 7 +
            engagement.tips_count * 10
        )
        
        # Apply time decay (reduce score for older content)
        hours_old = (datetime.utcnow() - engagement.created_at).total_seconds() / 3600
        time_decay = max(0.1, 1 - (hours_old / 168))  # Decay over a week
        
        engagement.trending_score = score * time_decay