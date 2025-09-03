"""
增强版预测API - 集成真实足球数据
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import os
import sys

# 添加backend目录到sys.path（如果还未添加）
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from services.football_api_client import FootballAPIClient, FootballDataAggregator
    from agents.football_prediction_writer import (
        FootballPredictionWriter,
        TeamInfo,
        MatchInfo,
        OddsInfo,
        HistoricalData
    )
except ImportError:
    # Fallback: Try importing from absolute path
    import importlib.util
    
    # Import football_api_client
    api_client_path = os.path.join(backend_dir, 'services', 'football_api_client.py')
    spec = importlib.util.spec_from_file_location("football_api_client", api_client_path)
    football_api_client = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(football_api_client)
    FootballAPIClient = football_api_client.FootballAPIClient
    FootballDataAggregator = football_api_client.FootballDataAggregator
    
    # Import football_prediction_writer
    writer_path = os.path.join(backend_dir, 'agents', 'football_prediction_writer.py')
    spec = importlib.util.spec_from_file_location("football_prediction_writer", writer_path)
    football_prediction_writer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(football_prediction_writer)
    FootballPredictionWriter = football_prediction_writer.FootballPredictionWriter
    TeamInfo = football_prediction_writer.TeamInfo
    MatchInfo = football_prediction_writer.MatchInfo
    OddsInfo = football_prediction_writer.OddsInfo
    HistoricalData = football_prediction_writer.HistoricalData

router = APIRouter(prefix="/predictions/enhanced", tags=["predictions-enhanced"])

# 请求模型
class PredictionRequest(BaseModel):
    home_team_id: int
    away_team_id: int
    league_id: int
    league_name: str
    match_time: str
    venue: str
    fixture_id: Optional[int] = None
    expert_confidence: int = 85
    use_ai_enhancement: bool = True

class QuickPredictionRequest(BaseModel):
    home_team_name: str
    away_team_name: str
    league_name: str
    match_time: str
    venue: Optional[str] = "主队主场"

# 全局API客户端
api_client = None

def get_api_client():
    global api_client
    if api_client is None:
        api_key = os.getenv('FOOTBALL_API_KEY', '91e2647e3d88e2b4340eeb841181413c')
        api_client = FootballAPIClient(api_key)
    return api_client

@router.post("/generate-with-data")
async def generate_prediction_with_real_data(request: PredictionRequest):
    """
    使用真实数据生成预测
    
    这个端点会：
    1. 从Football API获取真实的球队数据
    2. 获取历史交锋记录
    3. 获取伤病信息
    4. 获取实时赔率
    5. 生成专业的预测文章
    """
    try:
        # 获取API客户端
        client = get_api_client()
        aggregator = FootballDataAggregator(client)
        
        # 获取真实数据
        real_data = aggregator.prepare_prediction_data(
            home_team_id=request.home_team_id,
            away_team_id=request.away_team_id,
            league_id=request.league_id,
            fixture_id=request.fixture_id
        )
        
        # 创建写作器
        writer = FootballPredictionWriter()
        
        # 转换数据格式
        home_team = TeamInfo(
            name=real_data['home_team']['name'],
            recent_form=real_data['home_team']['recent_form'],
            league_position=real_data['home_team']['league_position'],
            home_away_record=real_data['home_team']['home_away_record'],
            key_players_status=real_data['home_team']['key_players_status'],
            recent_performance=real_data['home_team']['recent_performance']
        )
        
        away_team = TeamInfo(
            name=real_data['away_team']['name'],
            recent_form=real_data['away_team']['recent_form'],
            league_position=real_data['away_team']['league_position'],
            home_away_record=real_data['away_team']['home_away_record'],
            key_players_status=real_data['away_team']['key_players_status'],
            recent_performance=real_data['away_team']['recent_performance']
        )
        
        match_info = MatchInfo(
            home_team=home_team,
            away_team=away_team,
            league=request.league_name,
            match_time=request.match_time,
            venue=request.venue
        )
        
        odds_info = OddsInfo(
            home_win=real_data['odds_info']['home_win'],
            draw=real_data['odds_info']['draw'],
            away_win=real_data['odds_info']['away_win'],
            asian_handicap=real_data['odds_info'].get('asian_handicap', ''),
            over_under=real_data['odds_info'].get('over_under', '')
        )
        
        historical_data = HistoricalData(
            h2h_results=real_data['historical_data']['h2h_results'],
            home_team_home_record=real_data['historical_data']['home_team_home_record'],
            away_team_away_record=real_data['historical_data']['away_team_away_record']
        )
        
        # AI增强预测（如果启用）
        api_predictions = None
        if request.use_ai_enhancement:
            api_predictions = await get_ai_predictions(real_data)
        
        # 生成预测
        prediction = writer.generate_prediction(
            match_info=match_info,
            odds_info=odds_info,
            historical_data=historical_data,
            expert_confidence=request.expert_confidence,
            api_predictions=api_predictions
        )
        
        return {
            "status": "success",
            "data": {
                "prediction": prediction,
                "raw_data": real_data,
                "data_source": "API-Sports"
            },
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成预测失败: {str(e)}")

@router.post("/quick-predict")
async def quick_prediction(request: QuickPredictionRequest):
    """
    快速预测 - 使用球队名称
    
    不需要球队ID，通过名称匹配生成预测
    """
    try:
        # 创建写作器
        writer = FootballPredictionWriter()
        
        # 使用默认数据（实际应用中可以通过名称搜索获取ID）
        home_team = TeamInfo(
            name=request.home_team_name,
            recent_form=['W', 'W', 'D', 'L', 'W'],
            league_position=3,
            home_away_record="主场表现优异",
            key_players_status={},
            recent_performance="近期状态良好，主场优势明显"
        )
        
        away_team = TeamInfo(
            name=request.away_team_name,
            recent_form=['L', 'D', 'W', 'D', 'L'],
            league_position=8,
            home_away_record="客场表现一般",
            key_players_status={},
            recent_performance="客场作战能力有待提升"
        )
        
        match_info = MatchInfo(
            home_team=home_team,
            away_team=away_team,
            league=request.league_name,
            match_time=request.match_time,
            venue=request.venue
        )
        
        # 默认赔率
        odds_info = OddsInfo(
            home_win=2.20,
            draw=3.30,
            away_win=2.80,
            asian_handicap="主队-0.5",
            over_under="2.5"
        )
        
        # 模拟历史数据
        historical_data = HistoricalData(
            h2h_results=[
                {"date": "2024-03-15", "score": "2-1", "winner": "home"},
                {"date": "2023-11-20", "score": "1-1", "winner": "draw"},
                {"date": "2023-07-10", "score": "0-2", "winner": "away"},
            ],
            home_team_home_record=f"主场对{away_team.name}优势明显",
            away_team_away_record=f"客场对{home_team.name}表现一般"
        )
        
        # 生成预测
        prediction = writer.generate_prediction(
            match_info=match_info,
            odds_info=odds_info,
            historical_data=historical_data,
            expert_confidence=80
        )
        
        return {
            "status": "success",
            "data": prediction,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"快速预测失败: {str(e)}")

async def get_ai_predictions(match_data: Dict) -> Dict:
    """
    获取AI模型预测（集成Claude API）
    """
    try:
        import anthropic
        
        # 获取API密钥
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return None
            
        client = anthropic.Anthropic(api_key=api_key)
        
        # 构建提示
        prompt = f"""基于以下数据，预测比赛结果：
        
主队：{match_data['home_team']['name']}
- 联赛排名：第{match_data['home_team']['league_position']}位
- 近期战绩：{match_data['home_team']['recent_performance']}
- 主场战绩：{match_data['home_team']['home_away_record']}

客队：{match_data['away_team']['name']}
- 联赛排名：第{match_data['away_team']['league_position']}位
- 近期战绩：{match_data['away_team']['recent_performance']}
- 客场战绩：{match_data['away_team']['home_away_record']}

请给出：
1. 比赛结果预测（主胜/平/客胜）
2. 可能的比分
3. 简短理由（不超过50字）

请用JSON格式回复：{{"result": "主胜", "score": "2-1", "reason": "主场优势明显"}}"""

        # 调用Claude API
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=200,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # 解析响应
        import json
        ai_prediction = json.loads(response.content[0].text)
        
        return {
            "Claude AI": f"{ai_prediction['result']}，预测比分{ai_prediction['score']}",
            "AI分析": ai_prediction['reason']
        }
        
    except Exception as e:
        print(f"AI预测失败: {e}")
        return {
            "默认预测": "根据数据分析，主队略占优势"
        }

@router.get("/supported-leagues")
async def get_supported_leagues():
    """
    获取支持的联赛列表
    """
    leagues = [
        {"id": 39, "name": "英超", "country": "England"},
        {"id": 140, "name": "西甲", "country": "Spain"},
        {"id": 78, "name": "德甲", "country": "Germany"},
        {"id": 135, "name": "意甲", "country": "Italy"},
        {"id": 61, "name": "法甲", "country": "France"},
        {"id": 98, "name": "日职联", "country": "Japan"},
        {"id": 292, "name": "韩K联", "country": "South Korea"},
        {"id": 169, "name": "中超", "country": "China"},
    ]
    
    return {
        "status": "success",
        "data": leagues
    }

@router.get("/demo-teams")
async def get_demo_teams():
    """
    获取示例球队数据
    """
    teams = {
        "英超": [
            {"id": 33, "name": "曼联"},
            {"id": 50, "name": "曼城"},
            {"id": 3, "name": "利物浦"},
            {"id": 49, "name": "切尔西"},
            {"id": 42, "name": "阿森纳"},
        ],
        "西甲": [
            {"id": 541, "name": "皇家马德里"},
            {"id": 529, "name": "巴塞罗那"},
            {"id": 530, "name": "马德里竞技"},
        ],
        "日职联": [
            {"id": 302, "name": "浦和红钻"},
            {"id": 303, "name": "横滨水手"},
            {"id": 279, "name": "川崎前锋"},
        ]
    }
    
    return {
        "status": "success",
        "data": teams
    }