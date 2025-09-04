#!/usr/bin/env python
"""Render-optimized server startup script."""

import sys
import os
import logging
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set up basic logging for startup process
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def setup_data_directory():
    """Ensure data directory exists for SQLite database."""
    data_dir = Path("/data")
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created data directory: {data_dir}")
    
    # Also create local data directory as fallback
    local_data = backend_dir / "data"
    local_data.mkdir(exist_ok=True)

if __name__ == "__main__":
    try:
        # Setup data directory
        setup_data_directory()
        
        # Import after path setup
        import uvicorn
        from app.core.config import settings
        from app.core.database import init_db
        
        # Initialize database tables
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully!")
        
        # Log startup information
        logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
        logger.info(f"Environment: {settings.ENVIRONMENT}")
        logger.info(f"Host: {settings.HOST}, Port: {settings.PORT}")
        logger.info(f"Database URL: {settings.DATABASE_URL}")
        
        # Run the server
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=False,  # Disable reload in production
            log_level=settings.LOG_LEVEL.lower(),
            access_log=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)