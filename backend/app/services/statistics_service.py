"""Statistics service."""

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.domain.models import Statistics, Team, Match, Prediction, Expert


class StatisticsService:
    """Service for statistics-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_team_statistics(self, team_id: str, season: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get comprehensive team statistics."""
        team = self.db.query(Team).filter(Team.id == team_id).first()
        
        if not team:
            return None
        
        # Get all statistics for the team
        stats_query = self.db.query(Statistics).filter(Statistics.team_id == team_id)
        
        # Filter by season if provided
        if season:
            # This would need proper season filtering logic
            pass
        
        stats = stats_query.all()
        
        if not stats:
            return self._get_default_team_stats(team)
        
        # Aggregate statistics
        home_stats = [s for s in stats if s.is_home]
        away_stats = [s for s in stats if not s.is_home]
        
        return {
            "team": {
                "id": team.id,
                "name": team.name,
                "logo_url": team.logo_url,
                "league_position": team.league_position,
                "recent_form": team.recent_form
            },
            "overall": {
                "matches_played": len(stats),
                "avg_possession": self._calculate_average([s.possession for s in stats if s.possession]),
                "avg_shots": self._calculate_average([s.shots for s in stats if s.shots]),
                "avg_shots_on_target": self._calculate_average([s.shots_on_target for s in stats if s.shots_on_target]),
                "avg_pass_accuracy": self._calculate_average([s.pass_accuracy for s in stats if s.pass_accuracy]),
                "total_goals": sum([s.season_goals_scored for s in stats if s.season_goals_scored] or [0]),
                "total_goals_conceded": sum([s.season_goals_conceded for s in stats if s.season_goals_conceded] or [0]),
                "clean_sheets": sum([s.season_clean_sheets for s in stats if s.season_clean_sheets] or [0])
            },
            "home": {
                "matches_played": len(home_stats),
                "avg_possession": self._calculate_average([s.possession for s in home_stats if s.possession]),
                "avg_shots": self._calculate_average([s.shots for s in home_stats if s.shots]),
                "avg_goals_scored": self._calculate_average([s.season_avg_goals_scored for s in home_stats if s.season_avg_goals_scored])
            },
            "away": {
                "matches_played": len(away_stats),
                "avg_possession": self._calculate_average([s.possession for s in away_stats if s.possession]),
                "avg_shots": self._calculate_average([s.shots for s in away_stats if s.shots]),
                "avg_goals_scored": self._calculate_average([s.season_avg_goals_scored for s in away_stats if s.season_avg_goals_scored])
            },
            "recent_form": {
                "last_5_matches": team.recent_form,
                "form_goals_scored": stats[-1].form_goals_scored if stats else 0,
                "form_goals_conceded": stats[-1].form_goals_conceded if stats else 0
            }
        }
    
    def get_league_statistics(self, league_id: str, season: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get league-wide statistics."""
        # For simplicity, we'll use league name as ID
        matches = self.db.query(Match).filter(Match.league == league_id).all()
        
        if not matches:
            return None
        
        # Get all teams in the league
        team_ids = set()
        for match in matches:
            team_ids.add(match.home_team_id)
            team_ids.add(match.away_team_id)
        
        teams = self.db.query(Team).filter(Team.id.in_(team_ids)).all()
        
        # Calculate league statistics
        total_goals = sum([
            (match.home_score or 0) + (match.away_score or 0)
            for match in matches
            if match.status == "finished"
        ])
        
        finished_matches = [m for m in matches if m.status == "finished"]
        avg_goals_per_match = total_goals / len(finished_matches) if finished_matches else 0
        
        return {
            "league": {
                "id": league_id,
                "name": league_id,
                "season": season or "2023-24"
            },
            "statistics": {
                "total_matches": len(matches),
                "finished_matches": len(finished_matches),
                "total_goals": total_goals,
                "avg_goals_per_match": round(avg_goals_per_match, 2),
                "total_teams": len(teams)
            },
            "teams": [
                {
                    "id": team.id,
                    "name": team.name,
                    "position": team.league_position,
                    "recent_form": team.recent_form
                }
                for team in sorted(teams, key=lambda t: t.league_position or 999)[:10]
            ]
        }
    
    def get_betting_trends(self, period: str = "week", league: Optional[str] = None) -> Dict[str, Any]:
        """Get current betting trends."""
        # Calculate date filter
        date_filter = datetime.utcnow()
        if period == "day":
            date_filter = datetime.utcnow() - timedelta(days=1)
        elif period == "week":
            date_filter = datetime.utcnow() - timedelta(days=7)
        elif period == "month":
            date_filter = datetime.utcnow() - timedelta(days=30)
        
        # Get recent predictions
        query = self.db.query(Prediction).filter(Prediction.created_at >= date_filter)
        predictions = query.all()
        
        # Calculate trends
        prediction_types = {}
        for pred in predictions:
            pred_type = pred.prediction_type
            if pred_type not in prediction_types:
                prediction_types[pred_type] = {"count": 0, "correct": 0}
            prediction_types[pred_type]["count"] += 1
            if pred.is_correct:
                prediction_types[pred_type]["correct"] += 1
        
        # Get top experts
        top_experts = self.db.query(Expert).order_by(desc(Expert.win_rate)).limit(5).all()
        
        return {
            "period": period,
            "league": league,
            "trends": {
                "total_predictions": len(predictions),
                "prediction_types": prediction_types,
                "avg_confidence": self._calculate_average([p.confidence for p in predictions]),
                "success_rate": self._calculate_success_rate(predictions)
            },
            "top_experts": [
                {
                    "id": expert.id,
                    "name": expert.name,
                    "win_rate": expert.win_rate,
                    "total_predictions": expert.total_predictions
                }
                for expert in top_experts
            ],
            "popular_bets": self._get_popular_bets(predictions),
            "value_bets": self._get_value_bets(predictions)
        }
    
    def compare_teams(self, team1_id: str, team2_id: str) -> Optional[Dict[str, Any]]:
        """Compare statistics between two teams."""
        team1 = self.db.query(Team).filter(Team.id == team1_id).first()
        team2 = self.db.query(Team).filter(Team.id == team2_id).first()
        
        if not team1 or not team2:
            return None
        
        # Get statistics for both teams
        team1_stats = self.get_team_statistics(team1_id)
        team2_stats = self.get_team_statistics(team2_id)
        
        # Get head-to-head matches
        h2h_matches = self.db.query(Match).filter(
            ((Match.home_team_id == team1_id) & (Match.away_team_id == team2_id)) |
            ((Match.home_team_id == team2_id) & (Match.away_team_id == team1_id))
        ).order_by(desc(Match.match_date)).limit(10).all()
        
        team1_wins = 0
        team2_wins = 0
        draws = 0
        
        for match in h2h_matches:
            if match.status == "finished":
                if match.home_team_id == team1_id:
                    if match.home_score > match.away_score:
                        team1_wins += 1
                    elif match.home_score < match.away_score:
                        team2_wins += 1
                    else:
                        draws += 1
                else:
                    if match.home_score > match.away_score:
                        team2_wins += 1
                    elif match.home_score < match.away_score:
                        team1_wins += 1
                    else:
                        draws += 1
        
        return {
            "team1": {
                "id": team1.id,
                "name": team1.name,
                "logo_url": team1.logo_url,
                "statistics": team1_stats
            },
            "team2": {
                "id": team2.id,
                "name": team2.name,
                "logo_url": team2.logo_url,
                "statistics": team2_stats
            },
            "head_to_head": {
                "total_matches": len(h2h_matches),
                "team1_wins": team1_wins,
                "team2_wins": team2_wins,
                "draws": draws,
                "recent_matches": [
                    {
                        "id": match.id,
                        "date": match.match_date,
                        "home_team": match.home_team_id,
                        "away_team": match.away_team_id,
                        "score": f"{match.home_score}-{match.away_score}" if match.home_score is not None else "N/A"
                    }
                    for match in h2h_matches[:5]
                ]
            }
        }
    
    def _calculate_average(self, values: List[float]) -> float:
        """Calculate average of non-None values."""
        valid_values = [v for v in values if v is not None]
        return round(sum(valid_values) / len(valid_values), 2) if valid_values else 0.0
    
    def _calculate_success_rate(self, predictions: List[Prediction]) -> float:
        """Calculate success rate of predictions."""
        if not predictions:
            return 0.0
        
        correct = len([p for p in predictions if p.is_correct == True])
        return round(correct / len(predictions) * 100, 2)
    
    def _get_popular_bets(self, predictions: List[Prediction]) -> List[Dict[str, Any]]:
        """Get most popular bet types."""
        bet_counts = {}
        for pred in predictions:
            outcome = pred.predicted_outcome
            if outcome not in bet_counts:
                bet_counts[outcome] = 0
            bet_counts[outcome] += 1
        
        sorted_bets = sorted(bet_counts.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"outcome": bet, "count": count}
            for bet, count in sorted_bets[:5]
        ]
    
    def _get_value_bets(self, predictions: List[Prediction]) -> List[Dict[str, Any]]:
        """Get value bets based on odds and success rate."""
        value_bets = []
        for pred in predictions:
            if pred.odds and pred.confidence > 70:
                expected_value = (pred.confidence / 100) * pred.odds
                if expected_value > 1.5:  # Value threshold
                    value_bets.append({
                        "prediction_id": pred.id,
                        "outcome": pred.predicted_outcome,
                        "odds": pred.odds,
                        "confidence": pred.confidence,
                        "expected_value": round(expected_value, 2)
                    })
        
        return sorted(value_bets, key=lambda x: x["expected_value"], reverse=True)[:5]
    
    def _get_default_team_stats(self, team: Team) -> Dict[str, Any]:
        """Get default statistics structure for a team."""
        return {
            "team": {
                "id": team.id,
                "name": team.name,
                "logo_url": team.logo_url,
                "league_position": team.league_position,
                "recent_form": team.recent_form
            },
            "overall": {
                "matches_played": 0,
                "avg_possession": 0.0,
                "avg_shots": 0.0,
                "avg_shots_on_target": 0.0,
                "avg_pass_accuracy": 0.0,
                "total_goals": 0,
                "total_goals_conceded": 0,
                "clean_sheets": 0
            },
            "home": {
                "matches_played": 0,
                "avg_possession": 0.0,
                "avg_shots": 0.0,
                "avg_goals_scored": 0.0
            },
            "away": {
                "matches_played": 0,
                "avg_possession": 0.0,
                "avg_shots": 0.0,
                "avg_goals_scored": 0.0
            },
            "recent_form": {
                "last_5_matches": team.recent_form,
                "form_goals_scored": 0,
                "form_goals_conceded": 0
            }
        }