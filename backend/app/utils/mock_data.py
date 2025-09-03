"""Mock data generator for development."""

import random
import json
from datetime import datetime, timedelta
from typing import List
import uuid

from sqlalchemy.orm import Session

from app.domain.models import (
    Team, Expert, Match, Prediction, BettingOdds,
    Analysis, Statistics, Engagement
)

# Create a simple mock data generator without faker
class SimpleFaker:
    def __init__(self):
        self.first_names = ["张", "李", "王", "刘", "陈", "杨", "赵", "黄", "周", "吴"]
        self.last_names = ["伟", "强", "磊", "洋", "勇", "军", "杰", "涛", "明", "辉"]
        self.words = ["足球", "预测", "分析", "战术", "进攻", "防守", "中场", "前锋", "门将", "教练"]
        
    def name(self):
        return random.choice(self.first_names) + random.choice(self.last_names)
    
    def sentence(self, nb_words=10):
        return "".join(random.choices(self.words, k=min(nb_words, len(self.words))))
    
    def text(self, max_nb_chars=200):
        return "".join(random.choices(self.words, k=20))[:max_nb_chars]
    
    def paragraph(self, nb_sentences=3):
        return " ".join([self.sentence() for _ in range(nb_sentences)])
    
    def url(self):
        return f"https://example.com/{uuid.uuid4().hex[:8]}"

fake = SimpleFaker()


class MockDataGenerator:
    """Generate mock data for testing."""
    
    def __init__(self, db: Session):
        self.db = db
        self.teams = []
        self.experts = []
        self.matches = []
    
    def generate_all(self):
        """Generate all mock data."""
        print("Generating mock data...")
        self.generate_teams()
        self.generate_experts()
        self.generate_matches()
        self.generate_predictions()
        self.generate_betting_odds()
        self.generate_analysis()
        self.generate_statistics()
        self.generate_engagement()
        print("Mock data generation complete!")
    
    def generate_teams(self, count: int = 20):
        """Generate mock teams."""
        print(f"Generating {count} teams...")
        
        team_names = [
            "Manchester United", "Liverpool", "Chelsea", "Arsenal", "Manchester City",
            "Tottenham", "Leicester City", "West Ham", "Everton", "Newcastle",
            "Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Valencia",
            "Bayern Munich", "Dortmund", "RB Leipzig", "Juventus", "AC Milan"
        ]
        
        for i, name in enumerate(team_names[:count]):
            team = Team(
                id=str(uuid.uuid4()),
                name=name,
                code=name[:3].upper(),
                logo_url=f"https://example.com/logos/{name.lower().replace(' ', '_')}.png",
                country=random.choice(["England", "Spain", "Germany", "Italy"]),
                founded_year=random.randint(1880, 1950),
                stadium=f"{name} Stadium",
                league_position=i + 1,
                recent_form="".join(random.choices(["W", "D", "L"], k=5))
            )
            self.db.add(team)
            self.teams.append(team)
        
        self.db.commit()
    
    def generate_experts(self, count: int = 10):
        """Generate mock experts."""
        print(f"Generating {count} experts...")
        
        badges = [
            {"name": "Top Predictor", "icon": "🏆", "color": "gold"},
            {"name": "Win Streak", "icon": "🔥", "color": "red"},
            {"name": "High Roller", "icon": "💰", "color": "green"},
            {"name": "Analyst Pro", "icon": "📊", "color": "blue"}
        ]
        
        specializations = ["Premier League", "La Liga", "Champions League", "Serie A", "Bundesliga"]
        
        for _ in range(count):
            recent_form = []
            for _ in range(5):
                recent_form.append({
                    "date": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
                    "result": random.choice(["win", "loss", "push"]),
                    "profit": round(random.uniform(-100, 200), 2),
                    "odds": round(random.uniform(1.5, 4.0), 2)
                })
            
            expert = Expert(
                id=str(uuid.uuid4()),
                name=fake.name(),
                avatar_url=f"https://i.pravatar.cc/150?img={random.randint(1, 70)}",
                bio=fake.text(max_nb_chars=200),
                win_rate=round(random.uniform(45, 75), 2),
                avg_return=round(random.uniform(-5, 25), 2),
                total_predictions=random.randint(50, 500),
                successful_predictions=random.randint(25, 400),
                followers_count=random.randint(100, 10000),
                following_count=random.randint(10, 500),
                badges=random.sample(badges, k=random.randint(0, 3)),
                specializations=random.sample(specializations, k=random.randint(1, 3)),
                recent_form=recent_form
            )
            self.db.add(expert)
            self.experts.append(expert)
        
        self.db.commit()
    
    def generate_matches(self, count: int = 30):
        """Generate mock matches."""
        print(f"Generating {count} matches...")
        
        leagues = ["Premier League", "La Liga", "Champions League", "Serie A", "Bundesliga"]
        statuses = ["scheduled", "scheduled", "scheduled", "live", "finished"]
        
        for _ in range(count):
            home_team = random.choice(self.teams)
            away_team = random.choice([t for t in self.teams if t.id != home_team.id])
            status = random.choice(statuses)
            
            match_date = datetime.utcnow() + timedelta(
                days=random.randint(-7, 14),
                hours=random.randint(0, 23)
            )
            
            match = Match(
                id=str(uuid.uuid4()),
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                league=random.choice(leagues),
                match_date=match_date,
                status=status,
                venue=home_team.stadium,
                referee=fake.name(),
                attendance=random.randint(10000, 80000) if status == "finished" else None,
                home_score=random.randint(0, 4) if status == "finished" else None,
                away_score=random.randint(0, 4) if status == "finished" else None,
                round=f"Round {random.randint(1, 38)}",
                season="2023-24",
                importance_level=random.randint(1, 5),
                weather=random.choice(["Clear", "Cloudy", "Rainy", "Windy"])
            )
            self.db.add(match)
            self.matches.append(match)
        
        self.db.commit()
    
    def generate_predictions(self):
        """Generate mock predictions."""
        print("Generating predictions...")
        
        prediction_types = ["match_result", "over_under", "btts", "correct_score", "asian_handicap"]
        outcomes = {
            "match_result": ["home_win", "draw", "away_win"],
            "over_under": ["over_2.5", "under_2.5", "over_1.5", "under_1.5"],
            "btts": ["yes", "no"],
            "correct_score": ["1-0", "2-1", "1-1", "2-0", "0-1"],
            "asian_handicap": ["home_-0.5", "away_+0.5", "home_-1.5", "away_+1.5"]
        }
        stake_levels = ["low", "medium", "high"]
        
        for match in self.matches[:20]:  # Generate predictions for first 20 matches
            num_predictions = random.randint(2, 5)
            selected_experts = random.sample(self.experts, k=min(num_predictions, len(self.experts)))
            
            for expert in selected_experts:
                pred_type = random.choice(prediction_types)
                prediction = Prediction(
                    id=str(uuid.uuid4()),
                    match_id=match.id,
                    expert_id=expert.id,
                    prediction_type=pred_type,
                    predicted_outcome=random.choice(outcomes[pred_type]),
                    confidence=round(random.uniform(55, 95), 2),
                    stake_level=random.choice(stake_levels),
                    odds=round(random.uniform(1.5, 4.5), 2),
                    potential_return=round(random.uniform(50, 500), 2),
                    reasoning=fake.text(max_nb_chars=500),
                    key_factors=json.dumps([
                        "Recent form analysis",
                        "Head-to-head record",
                        "Team news and injuries",
                        "Tactical matchup"
                    ]),
                    is_correct=random.choice([True, False, None]) if match.status == "finished" else None,
                    actual_return=round(random.uniform(-100, 300), 2) if match.status == "finished" else None,
                    likes_count=random.randint(0, 1000),
                    comments_count=random.randint(0, 100)
                )
                self.db.add(prediction)
        
        self.db.commit()
    
    def generate_betting_odds(self):
        """Generate mock betting odds."""
        print("Generating betting odds...")
        
        bookmakers = ["Bet365", "William Hill", "Ladbrokes", "Betfair", "Paddy Power"]
        
        for match in self.matches[:25]:  # Generate odds for first 25 matches
            for bookmaker in random.sample(bookmakers, k=random.randint(2, 4)):
                odds = BettingOdds(
                    id=str(uuid.uuid4()),
                    match_id=match.id,
                    bookmaker=bookmaker,
                    home_win=round(random.uniform(1.2, 5.0), 2),
                    draw=round(random.uniform(2.5, 4.5), 2),
                    away_win=round(random.uniform(1.5, 6.0), 2),
                    over_2_5=round(random.uniform(1.6, 2.2), 2),
                    under_2_5=round(random.uniform(1.6, 2.2), 2),
                    btts_yes=round(random.uniform(1.7, 2.1), 2),
                    btts_no=round(random.uniform(1.7, 2.1), 2),
                    handicap_home_line=-0.5,
                    handicap_home_odds=round(random.uniform(1.8, 2.2), 2),
                    handicap_away_line=0.5,
                    handicap_away_odds=round(random.uniform(1.8, 2.2), 2)
                )
                self.db.add(odds)
        
        self.db.commit()
    
    def generate_analysis(self):
        """Generate mock analysis."""
        print("Generating analysis...")
        
        formations = ["4-3-3", "4-4-2", "3-5-2", "4-2-3-1", "5-3-2"]
        
        for match in self.matches[:20]:  # Generate analysis for first 20 matches
            h2h_meetings = []
            for i in range(5):
                h2h_meetings.append({
                    "date": (datetime.utcnow() - timedelta(days=random.randint(30, 365))).isoformat(),
                    "home_team": match.home_team.name if match.home_team else "Team A",
                    "away_team": match.away_team.name if match.away_team else "Team B",
                    "home_score": random.randint(0, 4),
                    "away_score": random.randint(0, 4),
                    "competition": random.choice(["League", "Cup", "Champions League"])
                })
            
            key_players = []
            for _ in range(3):
                key_players.append({
                    "name": fake.name(),
                    "position": random.choice(["Forward", "Midfielder", "Defender", "Goalkeeper"]),
                    "number": random.randint(1, 99),
                    "status": random.choice(["fit", "doubtful", "injured"]),
                    "importance": random.randint(3, 5)
                })
            
            analysis = Analysis(
                id=str(uuid.uuid4()),
                match_id=match.id,
                tactical_analysis=fake.text(max_nb_chars=1000),
                formation_home=random.choice(formations),
                formation_away=random.choice(formations),
                key_players_home=key_players,
                key_players_away=key_players,
                injuries_home=[],
                injuries_away=[],
                suspensions_home=[],
                suspensions_away=[],
                home_form_last_5="".join(random.choices(["W", "D", "L"], k=5)),
                away_form_last_5="".join(random.choices(["W", "D", "L"], k=5)),
                home_form_home="".join(random.choices(["W", "D", "L"], k=5)),
                away_form_away="".join(random.choices(["W", "D", "L"], k=5)),
                h2h_last_meetings=h2h_meetings,
                h2h_home_wins=random.randint(0, 5),
                h2h_draws=random.randint(0, 5),
                h2h_away_wins=random.randint(0, 5),
                h2h_avg_goals=round(random.uniform(1.5, 3.5), 2),
                statistical_edge=fake.text(max_nb_chars=500),
                predicted_goals_home=round(random.uniform(0.5, 3.0), 2),
                predicted_goals_away=round(random.uniform(0.5, 3.0), 2),
                sentiment_score=round(random.uniform(-1, 1), 2),
                match_importance_home=random.randint(1, 5),
                match_importance_away=random.randint(1, 5),
                venue_advantage=round(random.uniform(0.1, 0.3), 2)
            )
            self.db.add(analysis)
        
        self.db.commit()
    
    def generate_statistics(self):
        """Generate mock statistics."""
        print("Generating statistics...")
        
        for match in self.matches[:15]:  # Generate stats for first 15 matches
            # Home team statistics
            home_stats = Statistics(
                id=str(uuid.uuid4()),
                match_id=match.id,
                team_id=match.home_team_id,
                is_home=True,
                possession=round(random.uniform(35, 65), 1),
                passes=random.randint(300, 700),
                passes_accurate=random.randint(200, 600),
                pass_accuracy=round(random.uniform(70, 90), 1),
                shots=random.randint(5, 25),
                shots_on_target=random.randint(2, 15),
                shots_off_target=random.randint(2, 10),
                shots_blocked=random.randint(0, 5),
                shots_inside_box=random.randint(3, 15),
                shots_outside_box=random.randint(2, 10),
                corners=random.randint(2, 12),
                offsides=random.randint(0, 6),
                free_kicks=random.randint(5, 20),
                fouls=random.randint(5, 20),
                yellow_cards=random.randint(0, 4),
                red_cards=random.randint(0, 1),
                tackles=random.randint(10, 30),
                interceptions=random.randint(5, 20),
                saves=random.randint(1, 8),
                expected_goals=round(random.uniform(0.5, 3.0), 2),
                expected_goals_against=round(random.uniform(0.5, 2.5), 2),
                touches_in_box=random.randint(10, 40),
                dangerous_attacks=random.randint(20, 60),
                season_goals_scored=random.randint(20, 80),
                season_goals_conceded=random.randint(15, 60),
                season_clean_sheets=random.randint(5, 20),
                season_avg_goals_scored=round(random.uniform(1.0, 2.5), 2),
                season_avg_goals_conceded=round(random.uniform(0.8, 2.0), 2),
                form_goals_scored=random.randint(5, 20),
                form_goals_conceded=random.randint(3, 15),
                form_avg_possession=round(random.uniform(40, 60), 1),
                form_avg_shots=round(random.uniform(10, 20), 1)
            )
            self.db.add(home_stats)
            
            # Away team statistics
            away_stats = Statistics(
                id=str(uuid.uuid4()),
                match_id=match.id,
                team_id=match.away_team_id,
                is_home=False,
                possession=round(100 - home_stats.possession, 1),
                passes=random.randint(300, 700),
                passes_accurate=random.randint(200, 600),
                pass_accuracy=round(random.uniform(70, 90), 1),
                shots=random.randint(5, 25),
                shots_on_target=random.randint(2, 15),
                shots_off_target=random.randint(2, 10),
                shots_blocked=random.randint(0, 5),
                shots_inside_box=random.randint(3, 15),
                shots_outside_box=random.randint(2, 10),
                corners=random.randint(2, 12),
                offsides=random.randint(0, 6),
                free_kicks=random.randint(5, 20),
                fouls=random.randint(5, 20),
                yellow_cards=random.randint(0, 4),
                red_cards=random.randint(0, 1),
                tackles=random.randint(10, 30),
                interceptions=random.randint(5, 20),
                saves=random.randint(1, 8),
                expected_goals=round(random.uniform(0.5, 3.0), 2),
                expected_goals_against=round(random.uniform(0.5, 2.5), 2),
                touches_in_box=random.randint(10, 40),
                dangerous_attacks=random.randint(20, 60),
                season_goals_scored=random.randint(20, 80),
                season_goals_conceded=random.randint(15, 60),
                season_clean_sheets=random.randint(5, 20),
                season_avg_goals_scored=round(random.uniform(1.0, 2.5), 2),
                season_avg_goals_conceded=round(random.uniform(0.8, 2.0), 2),
                form_goals_scored=random.randint(5, 20),
                form_goals_conceded=random.randint(3, 15),
                form_avg_possession=round(random.uniform(40, 60), 1),
                form_avg_shots=round(random.uniform(10, 20), 1)
            )
            self.db.add(away_stats)
        
        self.db.commit()
    
    def generate_engagement(self):
        """Generate mock engagement data."""
        print("Generating engagement data...")
        
        for match in self.matches[:20]:  # Generate engagement for first 20 matches
            engagement = Engagement(
                id=str(uuid.uuid4()),
                match_id=match.id,
                views=random.randint(100, 50000),
                likes=random.randint(10, 5000),
                comments=random.randint(5, 500),
                shares=random.randint(2, 200),
                bookmarks=random.randint(5, 300),
                tips_count=random.randint(0, 50),
                tips_amount=round(random.uniform(0, 1000), 2),
                unique_visitors=random.randint(50, 30000),
                avg_time_spent=round(random.uniform(30, 300), 2),
                bounce_rate=round(random.uniform(20, 70), 2),
                trending_score=round(random.uniform(0, 100), 2)
            )
            self.db.add(engagement)
        
        self.db.commit()


def seed_database(db: Session):
    """Seed the database with mock data."""
    generator = MockDataGenerator(db)
    generator.generate_all()