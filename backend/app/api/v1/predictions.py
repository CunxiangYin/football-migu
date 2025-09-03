"""
预测内容生成API
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import sys
import os

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agents.football_prediction_writer import (
    FootballPredictionWriter,
    TeamInfo,
    MatchInfo,
    OddsInfo,
    HistoricalData
)

router = APIRouter(prefix="/predictions", tags=["predictions"])

# 请求模型
class TeamInfoRequest(BaseModel):
    name: str
    recent_form: list[str]
    league_position: int
    home_away_record: str
    key_players_status: Dict[str, str] = {}
    recent_performance: str

class MatchInfoRequest(BaseModel):
    home_team: TeamInfoRequest
    away_team: TeamInfoRequest
    league: str
    match_time: str
    venue: str
    weather: Optional[str] = None

class OddsInfoRequest(BaseModel):
    home_win: float
    draw: float
    away_win: float
    asian_handicap: str
    over_under: str

class HistoricalDataRequest(BaseModel):
    h2h_results: list[Dict[str, str]]
    home_team_home_record: str
    away_team_away_record: str

class GeneratePredictionRequest(BaseModel):
    match_info: MatchInfoRequest
    odds_info: OddsInfoRequest
    historical_data: HistoricalDataRequest
    expert_confidence: int = 80
    api_predictions: Optional[Dict] = None


@router.post("/generate", response_model=Dict[str, Any])
async def generate_prediction(request: GeneratePredictionRequest):
    """
    生成足球比赛预测内容
    
    根据提供的比赛信息、赔率、历史数据等，生成专业的预测分析文章。
    """
    try:
        writer = FootballPredictionWriter()
        
        # 转换请求数据为内部数据结构
        home_team = TeamInfo(
            name=request.match_info.home_team.name,
            recent_form=request.match_info.home_team.recent_form,
            league_position=request.match_info.home_team.league_position,
            home_away_record=request.match_info.home_team.home_away_record,
            key_players_status=request.match_info.home_team.key_players_status,
            recent_performance=request.match_info.home_team.recent_performance
        )
        
        away_team = TeamInfo(
            name=request.match_info.away_team.name,
            recent_form=request.match_info.away_team.recent_form,
            league_position=request.match_info.away_team.league_position,
            home_away_record=request.match_info.away_team.home_away_record,
            key_players_status=request.match_info.away_team.key_players_status,
            recent_performance=request.match_info.away_team.recent_performance
        )
        
        match_info = MatchInfo(
            home_team=home_team,
            away_team=away_team,
            league=request.match_info.league,
            match_time=request.match_info.match_time,
            venue=request.match_info.venue,
            weather=request.match_info.weather
        )
        
        odds_info = OddsInfo(
            home_win=request.odds_info.home_win,
            draw=request.odds_info.draw,
            away_win=request.odds_info.away_win,
            asian_handicap=request.odds_info.asian_handicap,
            over_under=request.odds_info.over_under
        )
        
        historical_data = HistoricalData(
            h2h_results=request.historical_data.h2h_results,
            home_team_home_record=request.historical_data.home_team_home_record,
            away_team_away_record=request.historical_data.away_team_away_record
        )
        
        # 生成预测
        prediction = writer.generate_prediction(
            match_info=match_info,
            odds_info=odds_info,
            historical_data=historical_data,
            expert_confidence=request.expert_confidence,
            api_predictions=request.api_predictions
        )
        
        return {
            "status": "success",
            "data": prediction,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/style-guide")
async def get_style_guide():
    """
    获取预测写作风格指南
    
    返回写作模板和专业词汇库
    """
    from agents.football_prediction_writer import PredictionStyleGuide
    
    guide = PredictionStyleGuide()
    return {
        "status": "success",
        "data": {
            "template": guide.get_writing_template(),
            "vocabulary": guide.get_vocabulary()
        }
    }


@router.post("/demo")
async def generate_demo_prediction():
    """
    生成示例预测
    
    使用预设数据生成一个完整的预测示例
    """
    writer = FootballPredictionWriter()
    
    # 示例数据
    home_team = TeamInfo(
        name="浦项制铁",
        recent_form=["W", "W", "D", "W", "L"],
        league_position=3,
        home_away_record="主场7胜2平1负",
        key_players_status={},
        recent_performance="近10场6胜2平2负，主场表现强势"
    )
    
    away_team = TeamInfo(
        name="全北现代",
        recent_form=["L", "W", "W", "D", "L"],
        league_position=5,
        home_away_record="客场3胜3平4负",
        key_players_status={"金英权": "伤缺", "李东炅": "状态不佳"},
        recent_performance="近10场4胜3平3负，客场表现起伏"
    )
    
    match_info = MatchInfo(
        home_team=home_team,
        away_team=away_team,
        league="韩K联",
        match_time="08/24 18:00",
        venue="浦项钢铁体育场",
        weather="晴，温度26℃"
    )
    
    odds_info = OddsInfo(
        home_win=2.28,
        draw=3.40,
        away_win=2.52,
        asian_handicap="主队-0.5",
        over_under="2.5/3"
    )
    
    historical_data = HistoricalData(
        h2h_results=[
            {"date": "2024-05-15", "score": "2-1", "winner": "home"},
            {"date": "2024-02-20", "score": "1-1", "winner": "draw"},
            {"date": "2023-11-08", "score": "3-2", "winner": "home"},
            {"date": "2023-08-15", "score": "0-1", "winner": "away"},
            {"date": "2023-05-10", "score": "2-2", "winner": "draw"}
        ],
        home_team_home_record="主场对全北现代5胜2平1负",
        away_team_away_record="客场对浦项制铁1胜2平5负"
    )
    
    # 模拟API预测
    api_predictions = {
        "AI模型A": "主队胜，比分2-1",
        "AI模型B": "主队让球胜，大球",
        "专家系统": "主队不败，推荐让球"
    }
    
    prediction = writer.generate_prediction(
        match_info=match_info,
        odds_info=odds_info,
        historical_data=historical_data,
        expert_confidence=88,
        api_predictions=api_predictions
    )
    
    return {
        "status": "success",
        "data": prediction,
        "generated_at": datetime.now().isoformat()
    }