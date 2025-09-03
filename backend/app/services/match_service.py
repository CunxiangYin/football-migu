"""Match service."""

from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_

from app.domain.models import Match, Team, Prediction, BettingOdds, Analysis, Statistics, Engagement
from app.domain.schemas import (
    MatchResponse, MatchDetail, MatchListItem,
    AnalysisResponse, StatisticsResponse,
    PredictionResponse, BettingOddsResponse
)


class MatchService:
    """Service for match-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_matches(
        self,
        league: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Tuple[List[MatchListItem], int]:
        """Get matches with filtering and pagination."""
        query = self.db.query(Match).options(
            joinedload(Match.home_team),
            joinedload(Match.away_team),
            joinedload(Match.engagement)
        )
        
        # Apply filters
        if league:
            query = query.filter(Match.league == league)
        if status:
            query = query.filter(Match.status == status)
        if date_from:
            query = query.filter(Match.match_date >= datetime.fromisoformat(date_from))
        if date_to:
            query = query.filter(Match.match_date <= datetime.fromisoformat(date_to))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * per_page
        matches = query.offset(offset).limit(per_page).all()
        
        # Convert to response schema
        result = []
        for match in matches:
            item = MatchListItem(
                id=match.id,
                home_team=match.home_team,
                away_team=match.away_team,
                league=match.league,
                match_date=match.match_date,
                status=match.status,
                home_score=match.home_score,
                away_score=match.away_score,
                predictions_count=len(match.predictions) if match.predictions else 0,
                trending_score=match.engagement.trending_score if match.engagement else 0.0
            )
            result.append(item)
        
        return result, total
    
    def get_match_detail(self, match_id: str) -> Optional[MatchDetail]:
        """Get detailed match information."""
        match = self.db.query(Match).options(
            joinedload(Match.home_team),
            joinedload(Match.away_team),
            joinedload(Match.predictions).joinedload(Prediction.expert),
            joinedload(Match.betting_odds),
            joinedload(Match.analysis),
            joinedload(Match.statistics),
            joinedload(Match.engagement)
        ).filter(Match.id == match_id).first()
        
        if not match:
            return None
        
        # Convert to detailed response
        return MatchDetail(
            id=match.id,
            home_team=match.home_team,
            away_team=match.away_team,
            league=match.league,
            match_date=match.match_date,
            status=match.status,
            venue=match.venue,
            referee=match.referee,
            home_score=match.home_score,
            away_score=match.away_score,
            round=match.round,
            season=match.season,
            importance_level=match.importance_level,
            weather=match.weather,
            attendance=match.attendance,
            created_at=match.created_at,
            updated_at=match.updated_at,
            predictions=[PredictionResponse.model_validate(p) for p in match.predictions] if match.predictions else [],
            betting_odds=[BettingOddsResponse.model_validate(o) for o in match.betting_odds] if match.betting_odds else [],
            analysis=AnalysisResponse.model_validate(match.analysis) if match.analysis else None,
            statistics=[StatisticsResponse.model_validate(s) for s in match.statistics] if match.statistics else [],
            engagement=match.engagement
        )
    
    def get_match_analysis(self, match_id: str) -> Optional[AnalysisResponse]:
        """Get match analysis."""
        analysis = self.db.query(Analysis).filter(
            Analysis.match_id == match_id
        ).first()
        
        if not analysis:
            return None
        
        return AnalysisResponse.model_validate(analysis)
    
    def get_match_statistics(self, match_id: str) -> List[StatisticsResponse]:
        """Get match statistics for both teams."""
        statistics = self.db.query(Statistics).options(
            joinedload(Statistics.team)
        ).filter(Statistics.match_id == match_id).all()
        
        result = []
        for stat in statistics:
            response = StatisticsResponse.model_validate(stat)
            response.team_name = stat.team.name if stat.team else None
            result.append(response)
        
        return result
    
    def get_match_predictions(self, match_id: str) -> List[PredictionResponse]:
        """Get all predictions for a match."""
        predictions = self.db.query(Prediction).options(
            joinedload(Prediction.expert)
        ).filter(Prediction.match_id == match_id).all()
        
        return [PredictionResponse.model_validate(p) for p in predictions]
    
    def get_match_odds(self, match_id: str) -> List[BettingOddsResponse]:
        """Get betting odds for a match."""
        odds = self.db.query(BettingOdds).filter(
            BettingOdds.match_id == match_id
        ).all()
        
        return [BettingOddsResponse.model_validate(o) for o in odds]