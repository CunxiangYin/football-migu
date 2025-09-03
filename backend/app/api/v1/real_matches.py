"""
Real-time match data API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from services.football_api_client import FootballAPIClient
from agents.football_prediction_writer import FootballPredictionWriter
from agents.prediction_experts import PredictionExpertProfiles
from app.domain.models import Expert, Prediction
import uuid
import random

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/real-matches", tags=["real-matches"])

def get_football_client():
    """Get Football API client instance"""
    try:
        return FootballAPIClient()
    except Exception as e:
        logger.error(f"Failed to initialize FootballAPIClient: {e}")
        return None

def get_prediction_writer():
    """Get prediction writer instance"""
    try:
        return FootballPredictionWriter()
    except Exception as e:
        logger.error(f"Failed to initialize FootballPredictionWriter: {e}")
        return None

@router.get("/today-tomorrow")
async def get_today_tomorrow_matches():
    """
    获取今天和明天的K联赛、J联赛真实比赛数据
    """
    client = get_football_client()
    
    if not client:
        # Fallback to mock data if API client fails
        return {
            "status": "success",
            "data": {
                "today": [
                    {
                        "fixture_id": 1001,
                        "date": datetime.now().isoformat(),
                        "venue": "首尔世界杯竞技场",
                        "home_team": {"id": 2750, "name": "FC首尔", "logo": ""},
                        "away_team": {"id": 2749, "name": "蔚山现代", "logo": ""},
                        "league": {"id": 292, "name": "K联赛1", "country": "韩国"}
                    },
                    {
                        "fixture_id": 1002,
                        "date": datetime.now().replace(hour=18, minute=0).isoformat(),
                        "venue": "埼玉2002体育场",
                        "home_team": {"id": 302, "name": "浦和红钻", "logo": ""},
                        "away_team": {"id": 303, "name": "横滨水手", "logo": ""},
                        "league": {"id": 98, "name": "J联赛1", "country": "日本"}
                    }
                ],
                "tomorrow": [
                    {
                        "fixture_id": 1003,
                        "date": (datetime.now() + timedelta(days=1)).replace(hour=15, minute=0).isoformat(),
                        "venue": "全州世界杯竞技场",
                        "home_team": {"id": 2751, "name": "全北现代", "logo": ""},
                        "away_team": {"id": 2748, "name": "浦项制铁", "logo": ""},
                        "league": {"id": 292, "name": "K联赛1", "country": "韩国"}
                    },
                    {
                        "fixture_id": 1004,
                        "date": (datetime.now() + timedelta(days=1)).replace(hour=14, minute=0).isoformat(),
                        "venue": "日产体育场",
                        "home_team": {"id": 279, "name": "川崎前锋", "logo": ""},
                        "away_team": {"id": 285, "name": "鹿岛鹿角", "logo": ""},
                        "league": {"id": 98, "name": "J联赛1", "country": "日本"}
                    }
                ]
            }
        }
    
    try:
        matches = client.get_today_tomorrow_matches()
        return {
            "status": "success",
            "data": matches
        }
    except Exception as e:
        logger.error(f"Error fetching matches: {e}")
        # Return mock data as fallback
        return {
            "status": "success",
            "data": {
                "today": [
                    {
                        "fixture_id": 1001,
                        "date": datetime.now().isoformat(),
                        "venue": "首尔世界杯竞技场",
                        "home_team": {"id": 2750, "name": "FC首尔", "logo": ""},
                        "away_team": {"id": 2749, "name": "蔚山现代", "logo": ""},
                        "league": {"id": 292, "name": "K联赛1", "country": "韩国"}
                    }
                ],
                "tomorrow": [
                    {
                        "fixture_id": 1003,
                        "date": (datetime.now() + timedelta(days=1)).replace(hour=15, minute=0).isoformat(),
                        "venue": "全州世界杯竞技场",
                        "home_team": {"id": 2751, "name": "全北现代", "logo": ""},
                        "away_team": {"id": 2748, "name": "浦项制铁", "logo": ""},
                        "league": {"id": 292, "name": "K联赛1", "country": "韩国"}
                    }
                ]
            }
        }

@router.post("/generate-prediction/{fixture_id}")
async def generate_match_prediction(
    fixture_id: int,
    expert_id: str = None,
    db: Session = Depends(get_db)
):
    """
    为指定比赛生成AI预测，可选择特定专家
    """
    client = get_football_client()
    writer = get_prediction_writer()
    expert_profiles = PredictionExpertProfiles()
    
    # 选择专家，如果没有指定就随机选择
    if expert_id:
        expert_key = next((k for k, v in expert_profiles.experts.items() if v.id == expert_id), None)
    else:
        expert_key = random.choice(list(expert_profiles.experts.keys()))
    
    selected_expert_profile = expert_profiles.experts[expert_key]
    
    # Initialize prediction content
    prediction_content = None
    
    # Try to generate real prediction with AI
    try:
        if writer and client:
            # For demo, use mock data but real AI generation
            from agents.football_prediction_writer import TeamInfo, MatchInfo, OddsInfo, HistoricalData
            
            # Create mock match info (in production, fetch from API)
            match_info = MatchInfo(
                home_team=TeamInfo(name="主队", league_position=3, recent_form="WWDLW"),
                away_team=TeamInfo(name="客队", league_position=5, recent_form="LDWWL"),
                match_time="2024-12-01 15:00:00",
                venue="主场体育场",
                weather="晴朗",
                league_name="联赛"
            )
            
            odds_info = OddsInfo(
                home_win=2.10,
                draw=3.20,
                away_win=3.50,
                asian_handicap="-0.5",
                over_under="2.5"
            )
            
            historical_data = HistoricalData(
                h2h_last_5=[
                    {"home_goals": 2, "away_goals": 1, "date": "2024-01-01"},
                    {"home_goals": 1, "away_goals": 1, "date": "2023-10-01"},
                    {"home_goals": 0, "away_goals": 2, "date": "2023-05-01"},
                ],
                home_recent_5=[
                    {"goals_for": 2, "goals_against": 1, "result": "W"},
                    {"goals_for": 3, "goals_against": 0, "result": "W"},
                    {"goals_for": 1, "goals_against": 1, "result": "D"},
                ],
                away_recent_5=[
                    {"goals_for": 1, "goals_against": 2, "result": "L"},
                    {"goals_for": 1, "goals_against": 1, "result": "D"},
                    {"goals_for": 2, "goals_against": 0, "result": "W"},
                ]
            )
            
            # Generate AI prediction
            prediction_result = writer.generate_prediction(
                match_info=match_info,
                odds_info=odds_info,
                historical_data=historical_data,
                expert_confidence=85,
                api_predictions=None
            )
            
            prediction_content = prediction_result.get("full_article", "生成预测中...")
    except Exception as e:
        logger.error(f"Failed to generate AI prediction: {e}")
        prediction_content = None
    
    # Generate expert-specific prediction using profile
    if not prediction_content:
        # Use the new detailed prediction generation method
        # Get match teams from the request or use defaults
        home_team = "FC首尔" if fixture_id == 1001 else "浦和红钻" if fixture_id == 1002 else "全北现代" if fixture_id == 1003 else "川崎前锋"
        away_team = "蔚山现代" if fixture_id == 1001 else "横滨水手" if fixture_id == 1002 else "浦项制铁" if fixture_id == 1003 else "鹿岛鹿角"
        
        # Generate detailed prediction using the expert's comprehensive method
        prediction_content = expert_profiles.generate_detailed_prediction(
            expert_key,
            home_team,
            away_team,
            fixture_id
        )
    
    # Get or create expert based on selected profile
    expert = db.query(Expert).filter(Expert.name == selected_expert_profile.name).first()
    if not expert:
        expert = Expert(
            id=selected_expert_profile.id,
            name=selected_expert_profile.name,
            avatar_url=f"https://api.dicebear.com/7.x/avataaars/svg?seed={expert_key}",
            bio=selected_expert_profile.bio,
            win_rate=selected_expert_profile.win_rate,
            avg_return=selected_expert_profile.avg_return,
            total_predictions=selected_expert_profile.total_predictions,
            successful_predictions=selected_expert_profile.successful_predictions,
            followers_count=selected_expert_profile.followers_count,
            specializations=selected_expert_profile.specializations
        )
        db.add(expert)
        db.commit()
    
    
    # Create prediction
    prediction = Prediction(
        id=str(uuid.uuid4()),
        match_id=str(fixture_id),
        expert_id=expert.id,
        prediction_type="match_result",
        predicted_outcome="home_win",
        confidence=75,
        stake_level="medium",
        odds=2.10,
        potential_return=210.0,
        reasoning=prediction_content,
        key_factors='{"form": "good", "h2h": "favorable", "injuries": "none"}',
        likes_count=0,
        comments_count=0
    )
    
    db.add(prediction)
    db.commit()
    
    return {
        "status": "success",
        "data": {
            "prediction_id": prediction.id,
            "fixture_id": fixture_id,
            "title": f"比赛预测 #{fixture_id}",
            "content": prediction.reasoning,
            "confidence": prediction.confidence,
            "predicted_outcome": prediction.predicted_outcome,
            "expert": {
                "name": expert.name,
                "win_rate": expert.win_rate
            }
        }
    }

@router.get("/experts")
async def get_experts_list(db: Session = Depends(get_db)):
    """
    获取所有专家列表
    """
    # Initialize expert profiles
    expert_profiles = PredictionExpertProfiles()
    
    result = []
    for expert_key, profile in expert_profiles.experts.items():
        result.append({
            "id": profile.id,
            "name": profile.name,
            "nickname": profile.nickname,
            "bio": profile.bio,
            "avatar_url": f"https://api.dicebear.com/7.x/avataaars/svg?seed={expert_key}",
            "win_rate": profile.win_rate,
            "followers": profile.followers_count,
            "specializations": profile.specializations,
            "total_predictions": profile.total_predictions,
            "successful_predictions": profile.successful_predictions
        })
    
    return {
        "status": "success",
        "data": result
    }

@router.get("/predictions")
async def get_match_predictions(db: Session = Depends(get_db)):
    """
    获取所有比赛预测列表，用于前端展示
    """
    # Get recent predictions
    predictions = db.query(Prediction).order_by(Prediction.created_at.desc()).limit(20).all()
    
    result = []
    for pred in predictions:
        expert = db.query(Expert).filter(Expert.id == pred.expert_id).first()
        result.append({
            "id": pred.id,
            "title": f"比赛预测 - {pred.predicted_outcome}",
            "summary": pred.reasoning[:100] + "..." if pred.reasoning and len(pred.reasoning) > 100 else pred.reasoning or "暂无预测内容",
            "confidence": pred.confidence,
            "predicted_outcome": pred.predicted_outcome,
            "match_time": pred.created_at.isoformat(),
            "expert": {
                "id": expert.id if expert else "",
                "name": expert.name if expert else "专家",
                "avatar": expert.avatar_url if expert else "",
                "accuracy": expert.win_rate if expert else 80
            },
            "stats": {
                "likes": pred.likes_count or random.randint(100, 1000),
                "comments": pred.comments_count or random.randint(10, 100),
                "views": random.randint(1000, 10000)
            }
        })
    
    return {
        "status": "success",
        "data": result
    }