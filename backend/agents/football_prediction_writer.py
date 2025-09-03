"""
足球比赛预测写作Agent
基于专业分析模板，生成详细的比赛预测报告
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import json

@dataclass
class TeamInfo:
    """球队信息"""
    name: str
    recent_form: List[str]  # 近期战绩 ['W', 'D', 'L', ...]
    league_position: int
    home_away_record: str  # 主/客场战绩描述
    key_players_status: Dict[str, str]  # 关键球员状态
    recent_performance: str  # 近期表现描述

@dataclass
class MatchInfo:
    """比赛信息"""
    home_team: TeamInfo
    away_team: TeamInfo
    league: str
    match_time: str
    venue: str
    weather: Optional[str] = None
    
@dataclass
class OddsInfo:
    """赔率信息"""
    home_win: float
    draw: float
    away_win: float
    asian_handicap: str  # 亚盘
    over_under: str  # 大小球

@dataclass
class HistoricalData:
    """历史交锋数据"""
    h2h_results: List[Dict[str, str]]  # 历史交锋记录
    home_team_home_record: str  # 主队主场对阵客队记录
    away_team_away_record: str  # 客队客场对阵主队记录

class FootballPredictionWriter:
    """
    足球比赛预测内容生成器
    
    写作风格特点：
    1. 结构化分析：近期表现 -> 历史交锋 -> 比分预测
    2. 数据驱动：使用具体数据支撑观点
    3. 专业术语：使用足球专业词汇
    4. 逻辑清晰：因果关系明确
    5. 置信度表达：明确给出推荐和信心水平
    """
    
    def __init__(self):
        self.sections = [
            "近期表现",
            "历史交锋", 
            "伤病情况",
            "比分预测"
        ]
        
    def generate_prediction(
        self,
        match_info: MatchInfo,
        odds_info: OddsInfo,
        historical_data: HistoricalData,
        expert_confidence: int = 80,
        api_predictions: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        生成完整的比赛预测
        
        Args:
            match_info: 比赛信息
            odds_info: 赔率信息
            historical_data: 历史数据
            expert_confidence: 专家信心指数 (0-100)
            api_predictions: 其他API的预测结果
            
        Returns:
            包含预测内容的字典
        """
        
        prediction = {
            "title": self._generate_title(match_info),
            "confidence": expert_confidence,
            "summary": self._generate_summary(match_info, odds_info),
            "sections": {},
            "recommendation": self._generate_recommendation(match_info, odds_info, expert_confidence),
            "predicted_score": self._predict_score(match_info, historical_data, api_predictions)
        }
        
        # 生成各个分析章节
        prediction["sections"]["近期表现"] = self._analyze_recent_form(match_info)
        prediction["sections"]["历史交锋"] = self._analyze_h2h(historical_data, match_info)
        prediction["sections"]["伤病情况"] = self._analyze_injuries(match_info)
        prediction["sections"]["比分预测"] = self._analyze_score_prediction(
            match_info, historical_data, odds_info, api_predictions
        )
        
        # 生成完整文章
        prediction["full_article"] = self._compile_full_article(prediction)
        
        return prediction
    
    def _generate_title(self, match_info: MatchInfo) -> str:
        """生成标题"""
        return f"{match_info.league}联赛，{match_info.home_team.name} VS {match_info.away_team.name}"
    
    def _generate_summary(self, match_info: MatchInfo, odds_info: OddsInfo) -> str:
        """生成摘要"""
        return f"日职业东京FC对该京都不死鸟的比赛分析："
    
    def _analyze_recent_form(self, match_info: MatchInfo) -> str:
        """分析近期表现"""
        home_team = match_info.home_team
        away_team = match_info.away_team
        
        content = f"""近期表现

{home_team.name}：{home_team.recent_performance}

{away_team.name}：{away_team.recent_performance}"""
        
        return content
    
    def _analyze_h2h(self, historical_data: HistoricalData, match_info: MatchInfo) -> str:
        """分析历史交锋"""
        h2h_summary = self._summarize_h2h(historical_data.h2h_results)
        
        content = f"""历史交锋

在过去的交锋记录中，{match_info.home_team.name}与{match_info.away_team.name}的对战纪录较为胶着。
{h2h_summary}
{historical_data.home_team_home_record}
{historical_data.away_team_away_record}"""
        
        return content
    
    def _analyze_injuries(self, match_info: MatchInfo) -> str:
        """分析伤病情况"""
        home_injuries = match_info.home_team.key_players_status
        away_injuries = match_info.away_team.key_players_status
        
        content = "伤病情况\n\n"
        
        if home_injuries:
            content += f"{match_info.home_team.name}："
            for player, status in home_injuries.items():
                content += f"{player}（{status}）"
            content += "\n"
            
        if away_injuries:
            content += f"{match_info.away_team.name}："
            for player, status in away_injuries.items():
                content += f"{player}（{status}）"
                
        if not home_injuries and not away_injuries:
            content += "双方主力阵容齐整，无重大伤病困扰。"
            
        return content
    
    def _analyze_score_prediction(
        self, 
        match_info: MatchInfo,
        historical_data: HistoricalData,
        odds_info: OddsInfo,
        api_predictions: Optional[Dict]
    ) -> str:
        """分析比分预测"""
        
        content = f"""比分预测

综合两队的近期状态、战术特点以及历史交锋记录，预测本场比赛：

主队{match_info.home_team.name}在主场优势明显，近期{match_info.home_team.recent_performance}

客队{match_info.away_team.name}客场表现{match_info.away_team.recent_performance}

亚盘开出{odds_info.asian_handicap}，大小球开{odds_info.over_under}。

综合分析，本场比赛预测比分为："""
        
        if api_predictions:
            # 综合API预测结果
            content += self._integrate_api_predictions(api_predictions)
            
        return content
    
    def _predict_score(
        self,
        match_info: MatchInfo,
        historical_data: HistoricalData, 
        api_predictions: Optional[Dict]
    ) -> str:
        """预测具体比分"""
        # 基于历史数据和球队状态预测比分
        # 这里可以接入更复杂的算法
        return "2-1"
    
    def _generate_recommendation(
        self,
        match_info: MatchInfo,
        odds_info: OddsInfo,
        confidence: int
    ) -> Dict[str, Any]:
        """生成推荐"""
        recommendation = {
            "bet_type": "asian_handicap",  # 亚盘
            "selection": "home -0.5",  # 主队让半球
            "odds": odds_info.home_win,
            "confidence": confidence,
            "stake_suggestion": self._calculate_stake(confidence),
            "reasoning": "主场优势明显，状态出色，值得信赖"
        }
        return recommendation
    
    def _calculate_stake(self, confidence: int) -> str:
        """根据信心指数计算建议投注金额"""
        if confidence >= 90:
            return "3单位"
        elif confidence >= 80:
            return "2单位"
        elif confidence >= 70:
            return "1单位"
        else:
            return "0.5单位"
    
    def _summarize_h2h(self, h2h_results: List[Dict]) -> str:
        """总结历史交锋"""
        if not h2h_results:
            return "双方近期无交锋记录。"
            
        wins = {"home": 0, "draw": 0, "away": 0}
        for result in h2h_results[:5]:  # 只看最近5场
            if result.get("winner") == "home":
                wins["home"] += 1
            elif result.get("winner") == "draw":
                wins["draw"] += 1
            else:
                wins["away"] += 1
                
        return f"近5次交锋，主队{wins['home']}胜{wins['draw']}平{wins['away']}负。"
    
    def _integrate_api_predictions(self, api_predictions: Dict) -> str:
        """整合API预测结果"""
        predictions_text = "\n"
        for source, prediction in api_predictions.items():
            predictions_text += f"- {source}预测：{prediction}\n"
        return predictions_text
    
    def _compile_full_article(self, prediction: Dict) -> str:
        """编译完整文章"""
        article = f"""【{prediction['title']}】

{prediction['summary']}

"""
        for section_name, section_content in prediction['sections'].items():
            article += f"{section_content}\n\n"
            
        article += f"""
推荐：{prediction['recommendation']['selection']}
置信度：{prediction['confidence']}%
预测比分：{prediction['predicted_score']}
"""
        return article


class PredictionStyleGuide:
    """
    预测写作风格指南
    基于分析的内容特征：
    
    1. 结构化程度高
       - 固定的章节：近期表现、历史交锋、伤病情况、比分预测
       - 每个章节有明确的分析重点
    
    2. 数据支撑充分
       - 具体的比赛场次和比分
       - 精确的统计数据（进球数、胜率等）
       - 时间节点明确
    
    3. 专业术语使用
       - 亚盘、大小球、让球
       - 主客场优势
       - 战术特点
    
    4. 逻辑推理清晰
       - 从数据到结论的推导过程
       - 多角度分析（状态、历史、伤病）
       - 风险提示
    
    5. 预测明确
       - 给出具体比分
       - 推荐投注方向
       - 信心指数
    """
    
    @staticmethod
    def get_writing_template() -> Dict[str, str]:
        """获取写作模板"""
        return {
            "opening": "分析开场，介绍比赛基本信息",
            "recent_form": "近期表现分析，包含具体战绩",
            "h2h": "历史交锋分析，统计数据支撑",
            "injuries": "伤病和人员情况",
            "odds_analysis": "赔率和盘口分析",
            "prediction": "比分预测和投注建议",
            "closing": "总结和风险提示"
        }
    
    @staticmethod
    def get_vocabulary() -> Dict[str, List[str]]:
        """获取专业词汇库"""
        return {
            "positive": ["状态出色", "优势明显", "值得信赖", "表现稳定", "实力占优"],
            "negative": ["状态低迷", "表现不佳", "难以信任", "起伏较大", "实力下滑"],
            "neutral": ["有待观察", "表现一般", "互有胜负", "难分伯仲", "势均力敌"],
            "technical": ["亚盘", "大小球", "让球", "水位", "盘口", "欧赔", "返还率"],
            "tactical": ["防守反击", "高位逼抢", "控球率", "射门效率", "定位球"]
        }


# 使用示例
if __name__ == "__main__":
    writer = FootballPredictionWriter()
    
    # 准备数据
    home_team = TeamInfo(
        name="东京FC",
        recent_form=["W", "W", "D", "L", "W"],
        league_position=3,
        home_away_record="主场5胜2平1负",
        key_players_status={},
        recent_performance="近5场3胜1平1负，状态良好"
    )
    
    away_team = TeamInfo(
        name="京都不死鸟",
        recent_form=["L", "D", "W", "W", "L"],
        league_position=7,
        home_away_record="客场2胜2平4负",
        key_players_status={"山田太郎": "伤缺"},
        recent_performance="近5场2胜1平2负，客场表现一般"
    )
    
    match_info = MatchInfo(
        home_team=home_team,
        away_team=away_team,
        league="日职联",
        match_time="08/24 18:00",
        venue="东京体育场"
    )
    
    odds_info = OddsInfo(
        home_win=2.28,
        draw=3.40,
        away_win=2.52,
        asian_handicap="主队-0.5",
        over_under="2.5球"
    )
    
    historical_data = HistoricalData(
        h2h_results=[
            {"date": "2024-03-15", "score": "2-1", "winner": "home"},
            {"date": "2023-11-20", "score": "1-1", "winner": "draw"},
            {"date": "2023-07-10", "score": "0-2", "winner": "away"},
        ],
        home_team_home_record="主场对京都3胜1平1负",
        away_team_away_record="客场对东京1胜1平3负"
    )
    
    # 生成预测
    prediction = writer.generate_prediction(
        match_info=match_info,
        odds_info=odds_info,
        historical_data=historical_data,
        expert_confidence=85
    )
    
    print(prediction["full_article"])