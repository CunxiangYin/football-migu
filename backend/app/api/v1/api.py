"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import matches, experts, statistics
from app.api.v1 import predictions, predictions_enhanced, real_matches

api_router = APIRouter()

# Include routers
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(experts.router, prefix="/experts", tags=["experts"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
api_router.include_router(predictions_enhanced.router, tags=["predictions-enhanced"])
api_router.include_router(real_matches.router, tags=["real-matches"])