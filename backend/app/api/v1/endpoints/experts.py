"""Expert endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.schemas import (
    ExpertResponse, ExpertStats,
    PredictionResponse,
    PaginationParams, PaginatedResponse,
    SuccessResponse
)
from app.domain.schemas.engagement import FollowRequest
from app.services.expert_service import ExpertService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[ExpertResponse])
async def get_experts(
    specialization: Optional[str] = Query(None, description="Filter by specialization"),
    min_win_rate: Optional[float] = Query(None, ge=0, le=100, description="Minimum win rate"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get list of experts with filtering and pagination.
    
    - **specialization**: Filter by league or team specialization
    - **min_win_rate**: Filter by minimum win rate percentage
    - **page**: Page number for pagination
    - **per_page**: Number of items per page
    """
    service = ExpertService(db)
    experts, total = service.get_experts(
        specialization=specialization,
        min_win_rate=min_win_rate,
        page=page,
        per_page=per_page
    )
    
    return PaginatedResponse.create(
        data=experts,
        page=page,
        per_page=per_page,
        total=total
    )


@router.get("/leaderboard", response_model=List[ExpertResponse])
async def get_expert_leaderboard(
    period: str = Query("all", pattern="^(week|month|all)$", description="Time period"),
    limit: int = Query(10, ge=1, le=50, description="Number of experts to return"),
    db: Session = Depends(get_db)
):
    """
    Get expert leaderboard ranked by performance.
    
    - **period**: Time period for ranking (week, month, all)
    - **limit**: Number of top experts to return
    """
    service = ExpertService(db)
    experts = service.get_leaderboard(period=period, limit=limit)
    
    return experts


@router.get("/{expert_id}", response_model=ExpertResponse)
async def get_expert(
    expert_id: str = Path(..., description="Expert ID"),
    db: Session = Depends(get_db)
):
    """
    Get detailed expert information.
    
    Returns:
    - Basic information (name, avatar, bio)
    - Performance statistics
    - Badges and achievements
    - Specializations
    - Recent form
    """
    service = ExpertService(db)
    expert = service.get_expert(expert_id)
    
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    return expert


@router.get("/{expert_id}/predictions", response_model=PaginatedResponse[PredictionResponse])
async def get_expert_predictions(
    expert_id: str = Path(..., description="Expert ID"),
    status: Optional[str] = Query(None, pattern="^(pending|correct|incorrect)$", description="Prediction status"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get expert's predictions with pagination.
    
    - **status**: Filter by prediction status
    - **page**: Page number for pagination
    - **per_page**: Number of items per page
    """
    service = ExpertService(db)
    predictions, total = service.get_expert_predictions(
        expert_id=expert_id,
        status=status,
        page=page,
        per_page=per_page
    )
    
    if predictions is None:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    return PaginatedResponse.create(
        data=predictions,
        page=page,
        per_page=per_page,
        total=total
    )


@router.get("/{expert_id}/statistics", response_model=ExpertStats)
async def get_expert_statistics(
    expert_id: str = Path(..., description="Expert ID"),
    period: str = Query("all", pattern="^(week|month|all)$", description="Time period"),
    db: Session = Depends(get_db)
):
    """
    Get expert's performance statistics.
    
    - **period**: Time period for statistics (week, month, all)
    
    Returns detailed performance metrics including:
    - Win rate
    - Average return
    - Total and successful predictions
    - Recent form
    - Trend analysis
    """
    service = ExpertService(db)
    stats = service.get_expert_statistics(expert_id, period)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    return stats


@router.post("/{expert_id}/follow", response_model=SuccessResponse)
async def follow_expert(
    request: FollowRequest,
    expert_id: str = Path(..., description="Expert ID"),
    db: Session = Depends(get_db)
):
    """
    Follow or unfollow an expert.
    
    - **action**: "follow" or "unfollow"
    """
    service = ExpertService(db)
    
    if request.action == "follow":
        success = service.follow_expert(expert_id, request.user_id)
        message = "Expert followed successfully"
    else:
        success = service.unfollow_expert(expert_id, request.user_id)
        message = "Expert unfollowed successfully"
    
    if not success:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    return SuccessResponse(
        message=message,
        data={"expert_id": expert_id, "action": request.action}
    )