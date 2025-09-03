#!/usr/bin/env python
"""Simple seed script without faker dependency."""

import sys
import os
import random
import uuid
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal, init_db
from app.domain.models import (
    Team, Expert, Match, Prediction, BettingOdds,
    Analysis, Statistics, Engagement
)


def seed_simple_data():
    """Seed database with simple mock data."""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Team).count() > 0:
            print("Database already contains data. Skipping seed.")
            return
        
        print("Seeding database with simple mock data...")
        
        # Create teams
        print("Creating teams...")
        teams = []
        team_names = [
            "Manchester United", "Liverpool", "Chelsea", "Arsenal",
            "Real Madrid", "Barcelona", "Bayern Munich", "Juventus"
        ]
        
        for name in team_names:
            team = Team(
                id=str(uuid.uuid4()),
                name=name,
                code=name[:3].upper(),
                logo_url=f"https://example.com/logos/{name.lower().replace(' ', '_')}.png",
                country="England" if "United" in name or "Liverpool" in name else "Spain",
                league_position=random.randint(1, 20),
                recent_form="WWDLW"
            )
            db.add(team)
            teams.append(team)
        
        db.commit()
        
        # Create experts
        print("Creating experts...")
        experts = []
        expert_names = ["John Smith", "Maria Garcia", "David Wilson", "Emma Johnson"]
        
        for name in expert_names:
            expert = Expert(
                id=str(uuid.uuid4()),
                name=name,
                avatar_url=f"https://i.pravatar.cc/150?u={name}",
                bio=f"Expert analyst specializing in football predictions",
                win_rate=round(random.uniform(55, 75), 2),
                avg_return=round(random.uniform(5, 25), 2),
                total_predictions=random.randint(100, 500),
                successful_predictions=random.randint(60, 400),
                followers_count=random.randint(500, 5000),
                badges=[{"name": "Top Predictor", "icon": "trophy", "color": "gold"}],
                specializations=["Premier League", "Champions League"]
            )
            db.add(expert)
            experts.append(expert)
        
        db.commit()
        
        # Create matches
        print("Creating matches...")
        matches = []
        for i in range(10):
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t.id != home_team.id])
            
            match = Match(
                id=str(uuid.uuid4()),
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                league="Premier League",
                match_date=datetime.utcnow() + timedelta(days=random.randint(1, 7)),
                status="scheduled",
                venue=f"{home_team.name} Stadium",
                season="2023-24",
                importance_level=random.randint(3, 5)
            )
            db.add(match)
            matches.append(match)
        
        db.commit()
        
        # Create predictions for first 5 matches
        print("Creating predictions...")
        for match in matches[:5]:
            for expert in experts[:2]:
                prediction = Prediction(
                    id=str(uuid.uuid4()),
                    match_id=match.id,
                    expert_id=expert.id,
                    prediction_type="match_result",
                    predicted_outcome=random.choice(["home_win", "draw", "away_win"]),
                    confidence=round(random.uniform(60, 90), 2),
                    stake_level="medium",
                    odds=round(random.uniform(1.5, 3.5), 2),
                    reasoning="Based on recent form and head-to-head statistics"
                )
                db.add(prediction)
        
        db.commit()
        
        # Create betting odds for first 5 matches
        print("Creating betting odds...")
        for match in matches[:5]:
            odds = BettingOdds(
                id=str(uuid.uuid4()),
                match_id=match.id,
                bookmaker="Bet365",
                home_win=round(random.uniform(1.5, 3.0), 2),
                draw=round(random.uniform(2.5, 3.5), 2),
                away_win=round(random.uniform(2.0, 4.0), 2),
                over_2_5=1.85,
                under_2_5=1.95,
                btts_yes=1.90,
                btts_no=1.90
            )
            db.add(odds)
        
        db.commit()
        
        # Create analysis for first 3 matches
        print("Creating analysis...")
        for match in matches[:3]:
            analysis = Analysis(
                id=str(uuid.uuid4()),
                match_id=match.id,
                tactical_analysis="Both teams prefer attacking football with high pressing",
                formation_home="4-3-3",
                formation_away="4-2-3-1",
                home_form_last_5="WWDWL",
                away_form_last_5="DWWLD",
                predicted_goals_home=1.8,
                predicted_goals_away=1.2,
                h2h_home_wins=3,
                h2h_draws=2,
                h2h_away_wins=1
            )
            db.add(analysis)
        
        db.commit()
        
        # Create engagement for first 5 matches
        print("Creating engagement data...")
        for match in matches[:5]:
            engagement = Engagement(
                id=str(uuid.uuid4()),
                match_id=match.id,
                views=random.randint(1000, 10000),
                likes=random.randint(100, 1000),
                comments=random.randint(10, 100),
                shares=random.randint(5, 50),
                trending_score=round(random.uniform(10, 90), 2)
            )
            db.add(engagement)
        
        db.commit()
        
        print("✅ Simple mock data seeded successfully!")
        
        # Print summary
        print(f"\nData Summary:")
        print(f"- Teams: {len(teams)}")
        print(f"- Experts: {len(experts)}")
        print(f"- Matches: {len(matches)}")
        print(f"- Predictions: {db.query(Prediction).count()}")
        print(f"- Betting Odds: {db.query(BettingOdds).count()}")
        print(f"- Analysis: {db.query(Analysis).count()}")
        print(f"- Engagement: {db.query(Engagement).count()}")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Initialize database tables
    init_db()
    
    # Seed data
    seed_simple_data()