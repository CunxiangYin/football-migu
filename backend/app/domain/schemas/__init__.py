"""Pydantic schemas package."""

from app.domain.schemas.expert import ExpertBase, ExpertCreate, ExpertUpdate, ExpertResponse, ExpertStats
from app.domain.schemas.match import MatchBase, MatchCreate, MatchUpdate, MatchResponse, MatchDetail, MatchListItem, TeamBase, TeamResponse
from app.domain.schemas.prediction import PredictionBase, PredictionCreate, PredictionResponse
from app.domain.schemas.betting import BettingOddsBase, BettingOddsCreate, BettingOddsResponse
from app.domain.schemas.analysis import AnalysisBase, AnalysisCreate, AnalysisResponse
from app.domain.schemas.statistics import StatisticsBase, StatisticsCreate, StatisticsResponse
from app.domain.schemas.engagement import EngagementBase, EngagementUpdate, EngagementResponse
from app.domain.schemas.common import PaginationParams, PaginatedResponse, SuccessResponse, ErrorResponse

__all__ = [
    # Expert
    "ExpertBase", "ExpertCreate", "ExpertUpdate", "ExpertResponse", "ExpertStats",
    # Match
    "MatchBase", "MatchCreate", "MatchUpdate", "MatchResponse", "MatchDetail", "MatchListItem",
    "TeamBase", "TeamResponse",
    # Prediction
    "PredictionBase", "PredictionCreate", "PredictionResponse",
    # Betting
    "BettingOddsBase", "BettingOddsCreate", "BettingOddsResponse",
    # Analysis
    "AnalysisBase", "AnalysisCreate", "AnalysisResponse",
    # Statistics
    "StatisticsBase", "StatisticsCreate", "StatisticsResponse",
    # Engagement
    "EngagementBase", "EngagementUpdate", "EngagementResponse",
    # Common
    "PaginationParams", "PaginatedResponse", "SuccessResponse", "ErrorResponse"
]