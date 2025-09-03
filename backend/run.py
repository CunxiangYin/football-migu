#!/usr/bin/env python
"""Run the application."""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from main import app
    import uvicorn
    from app.core.config import settings
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )