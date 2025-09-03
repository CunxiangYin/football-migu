#!/usr/bin/env python
"""Simple server startup script without mock data."""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings
    from app.core.database import init_db
    
    # Initialize database tables
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    
    print(f"\nStarting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Server running at http://{settings.HOST}:{settings.PORT}")
    print(f"API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"Health Check: http://{settings.HOST}:{settings.PORT}/health")
    print("\nPress CTRL+C to stop the server\n")
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )