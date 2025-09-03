"""Statistics endpoints."""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.schemas import StatisticsResponse, SuccessResponse
from app.services.statistics_service import StatisticsService

router = APIRouter()


@router.get("/teams/{team_id}", response_model=Dict[str, Any])
async def get_team_statistics(
    team_id: str = Path(..., description="Team ID"),
    season: Optional[str] = Query(None, description="Season (e.g., 2023-24)"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive team statistics.
    
    Returns:
    - Season statistics
    - Home/Away performance
    - Recent form
    - Goal statistics
    - Defensive statistics
    """
    service = StatisticsService(db)
    stats = service.get_team_statistics(team_id, season)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Team statistics not found")
    
    return stats


@router.get("/leagues/{league_id}", response_model=Dict[str, Any])
async def get_league_statistics(
    league_id: str = Path(..., description="League ID"),
    season: Optional[str] = Query(None, description="Season (e.g., 2023-24)"),
    db: Session = Depends(get_db)
):
    """
    Get league-wide statistics and trends.
    
    Returns:
    - League standings
    - Top scorers
    - Top assists
    - Team statistics comparison
    - League trends
    """
    service = StatisticsService(db)
    stats = service.get_league_statistics(league_id, season)
    
    if not stats:
        raise HTTPException(status_code=404, detail="League statistics not found")
    
    return stats


@router.get("/trends", response_model=Dict[str, Any])
async def get_betting_trends(
    period: str = Query("week", pattern="^(day|week|month)$", description="Time period"),
    league: Optional[str] = Query(None, description="Filter by league"),
    db: Session = Depends(get_db)
):
    """
    Get current betting trends and insights.
    
    - **period**: Time period for trends (day, week, month)
    - **league**: Filter trends by specific league
    
    Returns:
    - Popular bets
    - Winning streaks
    - Upset predictions
    - Value bets
    - Expert consensus
    """
    service = StatisticsService(db)
    trends = service.get_betting_trends(period, league)
    
    return trends


@router.get("/comparison", response_model=Dict[str, Any])
async def compare_teams(
    team1_id: str = Query(..., description="First team ID"),
    team2_id: str = Query(..., description="Second team ID"),
    db: Session = Depends(get_db)
):
    """
    Compare statistics between two teams.
    
    Returns head-to-head comparison including:
    - Historical matchups
    - Current form
    - Key statistics comparison
    - Strengths and weaknesses
    """
    service = StatisticsService(db)
    comparison = service.compare_teams(team1_id, team2_id)
    
    if not comparison:
        raise HTTPException(status_code=404, detail="One or both teams not found")
    
    return comparison