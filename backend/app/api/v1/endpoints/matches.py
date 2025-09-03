"""Match endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.schemas import (
    MatchResponse, MatchDetail, MatchListItem,
    AnalysisResponse, StatisticsResponse,
    PredictionResponse, BettingOddsResponse,
    PaginationParams, PaginatedResponse,
    SuccessResponse
)
from app.domain.schemas.engagement import LikeRequest
from app.services.match_service import MatchService
from app.services.engagement_service import EngagementService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[MatchListItem])
async def get_matches(
    league: Optional[str] = Query(None, description="Filter by league"),
    status: Optional[str] = Query(None, description="Filter by status"),
    date_from: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get list of matches with filtering and pagination.
    
    - **league**: Filter by league name
    - **status**: Filter by match status (scheduled, live, finished)
    - **date_from**: Filter matches from this date
    - **date_to**: Filter matches until this date
    - **page**: Page number for pagination
    - **per_page**: Number of items per page
    """
    service = MatchService(db)
    matches, total = service.get_matches(
        league=league,
        status=status,
        date_from=date_from,
        date_to=date_to,
        page=page,
        per_page=per_page
    )
    
    return PaginatedResponse.create(
        data=matches,
        page=page,
        per_page=per_page,
        total=total
    )


@router.get("/{match_id}", response_model=MatchDetail)
async def get_match(
    match_id: str = Path(..., description="Match ID"),
    db: Session = Depends(get_db)
):
    """
    Get detailed match information including all related data.
    
    Returns complete match details with:
    - Basic match information
    - Teams information
    - Predictions from experts
    - Betting odds from bookmakers
    - Match analysis
    - Statistics
    - Engagement metrics
    """
    service = MatchService(db)
    match = service.get_match_detail(match_id)
    
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return match


@router.get("/{match_id}/analysis", response_model=AnalysisResponse)
async def get_match_analysis(
    match_id: str = Path(..., description="Match ID"),
    db: Session = Depends(get_db)
):
    """
    Get detailed match analysis.
    
    Returns:
    - Tactical analysis
    - Team formations
    - Key players
    - Injury reports
    - Form analysis
    - Head-to-head statistics
    - Statistical predictions
    """
    service = MatchService(db)
    analysis = service.get_match_analysis(match_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found for this match")
    
    return analysis


@router.get("/{match_id}/statistics", response_model=List[StatisticsResponse])
async def get_match_statistics(
    match_id: str = Path(..., description="Match ID"),
    db: Session = Depends(get_db)
):
    """
    Get match statistics for both teams.
    
    Returns detailed statistics including:
    - Possession and passing stats
    - Shooting statistics
    - Defensive statistics
    - Set pieces
    - Advanced metrics (xG, xGA)
    - Season and form statistics
    """
    service = MatchService(db)
    statistics = service.get_match_statistics(match_id)
    
    if not statistics:
        raise HTTPException(status_code=404, detail="Statistics not found for this match")
    
    return statistics


@router.get("/{match_id}/predictions", response_model=List[PredictionResponse])
async def get_match_predictions(
    match_id: str = Path(..., description="Match ID"),
    db: Session = Depends(get_db)
):
    """
    Get all expert predictions for a match.
    
    Returns list of predictions with:
    - Expert information
    - Prediction type and outcome
    - Confidence level
    - Reasoning
    - Odds and potential returns
    """
    service = MatchService(db)
    predictions = service.get_match_predictions(match_id)
    
    return predictions


@router.get("/{match_id}/odds", response_model=List[BettingOddsResponse])
async def get_match_odds(
    match_id: str = Path(..., description="Match ID"),
    db: Session = Depends(get_db)
):
    """
    Get betting odds from various bookmakers.
    
    Returns odds for:
    - Match result (1X2)
    - Over/Under goals
    - Both teams to score
    - Asian handicap
    - Correct score
    - Double chance
    """
    service = MatchService(db)
    odds = service.get_match_odds(match_id)
    
    return odds


@router.post("/{match_id}/like", response_model=SuccessResponse)
async def like_match(
    match_id: str = Path(..., description="Match ID"),
    request: LikeRequest = None,
    db: Session = Depends(get_db)
):
    """
    Like a match or its predictions.
    
    Increments the like counter for the match engagement.
    """
    service = EngagementService(db)
    success = service.like_match(match_id, request.user_id if request else None)
    
    if not success:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return SuccessResponse(
        message="Match liked successfully",
        data={"match_id": match_id}
    )