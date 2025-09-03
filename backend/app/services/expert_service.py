"""Expert service."""

from typing import List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc

from app.domain.models import Expert, Prediction
from app.domain.schemas import ExpertResponse, ExpertStats, PredictionResponse


class ExpertService:
    """Service for expert-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_experts(
        self,
        specialization: Optional[str] = None,
        min_win_rate: Optional[float] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[ExpertResponse], int]:
        """Get experts with filtering and pagination."""
        query = self.db.query(Expert)
        
        # Apply filters
        if min_win_rate:
            query = query.filter(Expert.win_rate >= min_win_rate)
        
        # Filter by specialization (stored in JSON)
        if specialization:
            # This is a simplified version - in production, use PostgreSQL JSON operators
            # or filter in Python after fetching
            pass
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order by win rate
        offset = (page - 1) * per_page
        experts = query.order_by(desc(Expert.win_rate)).offset(offset).limit(per_page).all()
        
        # Convert to response schema
        result = [ExpertResponse.model_validate(expert) for expert in experts]
        
        return result, total
    
    def get_expert(self, expert_id: str) -> Optional[ExpertResponse]:
        """Get expert details."""
        expert = self.db.query(Expert).filter(Expert.id == expert_id).first()
        
        if not expert:
            return None
        
        return ExpertResponse.model_validate(expert)
    
    def get_expert_predictions(
        self,
        expert_id: str,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[Optional[List[PredictionResponse]], int]:
        """Get expert's predictions."""
        # Check if expert exists
        expert = self.db.query(Expert).filter(Expert.id == expert_id).first()
        if not expert:
            return None, 0
        
        query = self.db.query(Prediction).options(
            joinedload(Prediction.match),
            joinedload(Prediction.expert)
        ).filter(Prediction.expert_id == expert_id)
        
        # Apply status filter
        if status == "pending":
            query = query.filter(Prediction.is_correct.is_(None))
        elif status == "correct":
            query = query.filter(Prediction.is_correct == True)
        elif status == "incorrect":
            query = query.filter(Prediction.is_correct == False)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order by creation date
        offset = (page - 1) * per_page
        predictions = query.order_by(desc(Prediction.created_at)).offset(offset).limit(per_page).all()
        
        # Convert to response schema
        result = [PredictionResponse.model_validate(p) for p in predictions]
        
        return result, total
    
    def get_expert_statistics(self, expert_id: str, period: str = "all") -> Optional[ExpertStats]:
        """Get expert performance statistics."""
        expert = self.db.query(Expert).filter(Expert.id == expert_id).first()
        
        if not expert:
            return None
        
        # Calculate period filter
        date_filter = None
        if period == "week":
            date_filter = datetime.utcnow() - timedelta(days=7)
        elif period == "month":
            date_filter = datetime.utcnow() - timedelta(days=30)
        
        # Get predictions for the period
        query = self.db.query(Prediction).filter(Prediction.expert_id == expert_id)
        if date_filter:
            query = query.filter(Prediction.created_at >= date_filter)
        
        predictions = query.all()
        
        # Calculate statistics
        total = len(predictions)
        correct = len([p for p in predictions if p.is_correct == True])
        win_rate = (correct / total * 100) if total > 0 else 0
        
        # Calculate average return
        returns = [p.actual_return for p in predictions if p.actual_return is not None]
        avg_return = sum(returns) / len(returns) if returns else 0
        
        return ExpertStats(
            win_rate=win_rate,
            avg_return=avg_return,
            total_predictions=total,
            successful_predictions=correct,
            followers_count=expert.followers_count,
            recent_form=expert.recent_form or []
        )
    
    def get_leaderboard(self, period: str = "all", limit: int = 10) -> List[ExpertResponse]:
        """Get expert leaderboard."""
        query = self.db.query(Expert)
        
        # For now, just order by win rate
        # In production, calculate composite score based on period
        experts = query.order_by(desc(Expert.win_rate)).limit(limit).all()
        
        return [ExpertResponse.model_validate(expert) for expert in experts]
    
    def follow_expert(self, expert_id: str, user_id: Optional[str] = None) -> bool:
        """Follow an expert."""
        expert = self.db.query(Expert).filter(Expert.id == expert_id).first()
        
        if not expert:
            return False
        
        expert.followers_count += 1
        self.db.commit()
        
        return True
    
    def unfollow_expert(self, expert_id: str, user_id: Optional[str] = None) -> bool:
        """Unfollow an expert."""
        expert = self.db.query(Expert).filter(Expert.id == expert_id).first()
        
        if not expert:
            return False
        
        if expert.followers_count > 0:
            expert.followers_count -= 1
            self.db.commit()
        
        return True