"""Main application entry point."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from app.core.config import settings
from app.core.database import init_db, get_db
from app.core.logging import setup_logging
from app.api.v1.api import api_router
from app.utils.mock_data import seed_database


# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Seed database with mock data in development
    if settings.ENVIRONMENT == "development":
        try:
            from sqlalchemy.orm import Session
            from app.core.database import SessionLocal
            from app.domain.models import Team
            
            db = SessionLocal()
            # Check if data already exists
            if db.query(Team).count() == 0:
                logger.info("Seeding database with mock data...")
                seed_database(db)
                logger.info("Mock data seeded successfully")
            else:
                logger.info("Database already contains data, skipping seed")
            db.close()
        except Exception as e:
            logger.error(f"Error seeding database: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle global exceptions."""
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": str(exc) if settings.DEBUG else None
            }
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )