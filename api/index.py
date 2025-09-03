"""
Vercel Serverless Function wrapper for FastAPI backend
This allows deploying the Python backend to Vercel
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

# Import the FastAPI app
from backend.main import app

# Export handler for Vercel
handler = app