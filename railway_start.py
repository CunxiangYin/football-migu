#!/usr/bin/env python
"""Simple Railway startup script."""

import os
import sys

# Add backend to path
sys.path.insert(0, '/app/backend')

# Set working directory
os.chdir('/app/backend')

# Import and run
from main import app
import uvicorn

if __name__ == "__main__":
    # Get port from environment
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )