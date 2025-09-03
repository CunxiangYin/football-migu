#!/usr/bin/env python
"""Test script to verify backend setup."""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.core.config import settings
        print("✓ Configuration loaded")
        
        from app.core.database import Base, get_db
        print("✓ Database configuration loaded")
        
        from app.domain.models import Team, Expert, Match
        print("✓ Models loaded")
        
        from app.domain.schemas import MatchResponse, ExpertResponse
        print("✓ Schemas loaded")
        
        from app.services import MatchService, ExpertService
        print("✓ Services loaded")
        
        from app.api.v1.api import api_router
        print("✓ API routes loaded")
        
        from main import app
        print("✓ FastAPI app created")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import error: {e}")
        return False


def test_database():
    """Test database connection."""
    print("\nTesting database...")
    
    try:
        from app.core.database import engine, Base
        from sqlalchemy import inspect
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Check if tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['teams', 'experts', 'matches', 'predictions', 
                          'betting_odds', 'analysis', 'statistics', 'engagement']
        
        for table in expected_tables:
            if table in tables:
                print(f"✓ Table '{table}' exists")
            else:
                print(f"✗ Table '{table}' missing")
        
        print("\n✅ Database setup successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database error: {e}")
        return False


def test_api_routes():
    """Test API route registration."""
    print("\nTesting API routes...")
    
    try:
        from main import app
        
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        important_routes = [
            "/health",
            "/api/v1/matches",
            "/api/v1/experts",
            "/api/v1/statistics/trends"
        ]
        
        for route in important_routes:
            if any(route in r for r in routes):
                print(f"✓ Route '{route}' registered")
            else:
                print(f"✗ Route '{route}' missing")
        
        print(f"\nTotal routes registered: {len(routes)}")
        print("\n✅ API routes setup successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ API routes error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("Football Betting Backend Setup Test")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(test_imports())
    results.append(test_database())
    results.append(test_api_routes())
    
    # Summary
    print("\n" + "=" * 50)
    if all(results):
        print("✅ ALL TESTS PASSED - Backend is ready to run!")
        print("\nTo start the server, run:")
        print("  python run.py")
        print("\nThen visit:")
        print("  - API Docs: http://localhost:8000/docs")
        print("  - Health Check: http://localhost:8000/health")
    else:
        print("❌ SOME TESTS FAILED - Please check the errors above")
    print("=" * 50)