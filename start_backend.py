#!/usr/bin/env python
"""Railway startup script for backend."""

import sys
import os

# Set environment variable for database location first
os.environ["DATABASE_URL"] = "sqlite:///app/data/football_betting.db"

# Add backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

# Now import and run the server
if __name__ == "__main__":
    # Change to backend directory for imports to work
    os.chdir(backend_dir)
    
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
    
    # Run the server - use full module path
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,  # Disable reload in production
        log_level=settings.LOG_LEVEL.lower()
    )