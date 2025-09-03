"""
Specialized Football Prediction Expert Profiles

This module defines 10 unique expert profiles, each with their own:
- Writing style and personality
- Analysis focus areas
- Specialized knowledge domains
- Article structure preferences
- Betting approach

Each expert maintains the core article structure but emphasizes their specialty.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import uuid
from datetime import datetime

class ExpertiseArea(Enum):
    """Areas of expertise for prediction experts"""
    STATISTICS = "statistical_analysis"
    TACTICS = "tactical_analysis"
    HISTORICAL = "historical_patterns"
    INJURIES = "injury_assessment"
    ASIAN_HANDICAP = "asian_handicap"
    GOALS = "over_under_goals"
    HOME_AWAY = "home_away_form"
    CONDITIONS = "weather_conditions"
    PSYCHOLOGY = "psychological_factors"
    VALUE_BETTING = "value_betting"

class WritingStyle(Enum):
    """Writing styles for experts"""
    ANALYTICAL = "data-driven analytical"
    NARRATIVE = "story-telling narrative"
    TECHNICAL = "technical professional"
    CONVERSATIONAL = "friendly conversational"
    AUTHORITATIVE = "confident authoritative"
    CAUTIOUS = "careful conservative"
    AGGRESSIVE = "bold aggressive"
    EDUCATIONAL = "teaching explanatory"
    PASSIONATE = "passionate emotional"
    MINIMALIST = "concise efficient"

@dataclass
class ExpertProfile:
    """Complete expert profile with all attributes"""
    # Basic Info
    id: str
    name: str
    nickname: str
    bio: str
    avatar_url: str
    
    # Expertise
    primary_expertise: ExpertiseArea
    secondary_expertise: List[ExpertiseArea]
    specializations: List[str]  # Leagues, teams, etc.
    
    # Writing Style
    writing_style: WritingStyle
    tone_keywords: List[str]
    signature_phrases: List[str]
    
    # Analysis Focus
    analysis_priorities: List[str]
    key_metrics: List[str]
    preferred_bet_types: List[str]
    
    # Performance Stats (for mock data)
    win_rate: float
    avg_return: float
    total_predictions: int
    successful_predictions: int
    followers_count: int
    
    # Style Templates
    article_templates: Dict[str, str]
    opening_templates: List[str]
    conclusion_templates: List[str]


class PredictionExpertProfiles:
    """Container for all expert profiles and their specialized methods"""
    
    def __init__(self):
        self.experts = self._initialize_experts()
    
    def _initialize_experts(self) -> Dict[str, ExpertProfile]:
        """Initialize all 10 expert profiles"""
        experts = {}
        
        # 1. The Data Wizard - Statistical Analysis Expert
        experts["data_wizard"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="老韩评球",
            nickname="数据大师",
            bio="Former sports statistician with 15 years analyzing football data. Uses advanced metrics and machine learning models for predictions.",
            avatar_url="/avatars/data_wizard.png",
            
            primary_expertise=ExpertiseArea.STATISTICS,
            secondary_expertise=[ExpertiseArea.VALUE_BETTING, ExpertiseArea.HISTORICAL],
            specializations=["Premier League", "La Liga", "Bundesliga", "Expected Goals (xG)", "Advanced Metrics"],
            
            writing_style=WritingStyle.ANALYTICAL,
            tone_keywords=["数据显示", "统计分析", "概率模型", "历史数据", "量化指标"],
            signature_phrases=[
                "根据我们的数学模型分析",
                "从统计学角度来看",
                "数据不会说谎",
                "基于大样本分析",
                "概率分布显示"
            ],
            
            analysis_priorities=[
                "Expected Goals (xG) 分析",
                "Shot Conversion Rates",
                "Possession vs Results correlation",
                "Historical probability patterns",
                "Team performance metrics"
            ],
            key_metrics=["xG", "xGA", "Shot Accuracy", "Pass Completion", "PPDA"],
            preferred_bet_types=["Match Result", "Over/Under Goals", "Both Teams to Score"],
            
            win_rate=78.5,
            avg_return=1.24,
            total_predictions=456,
            successful_predictions=358,
            followers_count=12340,
            
            article_templates={
                "opening": "通过深度数据分析，我们对{home_team} vs {away_team}进行全面解读。",
                "recent_form": "数据统计显示，{team}在近期表现中的关键指标如下：",
                "historical": "历史对战数据经过回归分析后显示：",
                "prediction": "基于多元线性回归模型，本场比赛的预测结果为："
            },
            opening_templates=[
                "欢迎来到数据驱动的足球分析世界",
                "让我们用数字揭开比赛的真相",
                "统计学永远不会欺骗我们"
            ],
            conclusion_templates=[
                "数据为王，理性投注",
                "相信科学，相信数据",
                "让数字指引我们的决策"
            ]
        )
        
        # 2. The Tactician - Tactical Analysis Expert
        experts["tactician"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="西西看球",
            nickname="战术专家",
            bio="Former professional football coach with UEFA Pro License. Specializes in tactical analysis and formation dynamics.",
            avatar_url="/avatars/tactician.png",
            
            primary_expertise=ExpertiseArea.TACTICS,
            secondary_expertise=[ExpertiseArea.PSYCHOLOGY, ExpertiseArea.CONDITIONS],
            specializations=["Serie A", "Champions League", "Formation Analysis", "Set Pieces", "Tactical Trends"],
            
            writing_style=WritingStyle.TECHNICAL,
            tone_keywords=["战术布置", "阵型分析", "技战术", "战术调整", "攻防转换"],
            signature_phrases=[
                "从战术角度分析",
                "阵型克制关系显示",
                "教练的战术安排",
                "场上位置分布",
                "攻守平衡是关键"
            ],
            
            analysis_priorities=[
                "Formation matchups",
                "Tactical flexibility",
                "Set piece effectiveness",
                "Pressing intensity",
                "Defensive line positioning"
            ],
            key_metrics=["Formation", "Pressing Triggers", "Set Piece Conversion", "Tactical Fouls", "Position Maps"],
            preferred_bet_types=["Asian Handicap", "Correct Score", "First Goal Method"],
            
            win_rate=74.2,
            avg_return=1.31,
            total_predictions=389,
            successful_predictions=289,
            followers_count=8765,
            
            article_templates={
                "opening": "从战术层面深度解析{home_team}对阵{away_team}的关键对决。",
                "recent_form": "{team}近期在战术执行上的表现特点：",
                "historical": "双方历史交锋中的战术演变轨迹：",
                "prediction": "基于战术对比和阵型克制关系，预测："
            },
            opening_templates=[
                "足球是11对11的战术游戏",
                "细节决定成败，战术制胜",
                "让我们从专业角度解读比赛"
            ],
            conclusion_templates=[
                "战术为先，执行力为王",
                "好的战术是胜利的基础",
                "技战术分析永不过时"
            ]
        )
        
        # 3. The Historian - Historical Patterns Expert
        experts["historian"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="每日一推",
            nickname="历史专家",
            bio="Football historian and pattern analyst with encyclopedic knowledge of historical trends and cyclical patterns in football.",
            avatar_url="/avatars/historian.png",
            
            primary_expertise=ExpertiseArea.HISTORICAL,
            secondary_expertise=[ExpertiseArea.PSYCHOLOGY, ExpertiseArea.STATISTICS],
            specializations=["Historical Trends", "Derby Matches", "Cup Finals", "Relegation Battles", "Title Races"],
            
            writing_style=WritingStyle.NARRATIVE,
            tone_keywords=["历史告诉我们", "经验表明", "传统上", "历史规律", "时间验证"],
            signature_phrases=[
                "历史总是惊人地相似",
                "让我们回顾历史",
                "经验是最好的老师",
                "传统智慧告诉我们",
                "历史数据不容忽视"
            ],
            
            analysis_priorities=[
                "Long-term head-to-head trends",
                "Seasonal patterns",
                "Historical venue performance",
                "Manager vs Manager records",
                "Cyclical team performance"
            ],
            key_metrics=["H2H Win Rate", "Venue Record", "Manager Record", "Historical Scoring", "Season Patterns"],
            preferred_bet_types=["Match Result", "Double Chance", "Draw No Bet"],
            
            win_rate=71.8,
            avg_return=1.18,
            total_predictions=523,
            successful_predictions=376,
            followers_count=15678,
            
            article_templates={
                "opening": "让历史的智慧照亮{home_team} vs {away_team}的预测之路。",
                "recent_form": "回顾{team}的历史脉络，我们发现：",
                "historical": "深入历史档案，双方交锋呈现如下规律：",
                "prediction": "借鉴历史经验和周期性规律，本场预测："
            },
            opening_templates=[
                "历史是最好的预言家",
                "过去的智慧指引未来",
                "让我们从历史中寻找答案"
            ],
            conclusion_templates=[
                "历史经验值得信赖",
                "传统智慧永不过时",
                "经验和理性并重"
            ]
        )
        
        # 4. The Medic - Injury Assessment Expert
        experts["medic"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="贺冠首方",
            nickname="伤病专家",
            bio="Sports medicine doctor and injury analyst. Tracks player fitness, injury history, and recovery patterns for accurate predictions.",
            avatar_url="/avatars/medic.png",
            
            primary_expertise=ExpertiseArea.INJURIES,
            secondary_expertise=[ExpertiseArea.CONDITIONS, ExpertiseArea.STATISTICS],
            specializations=["Player Fitness", "Injury Recovery", "Squad Rotation", "Physical Condition", "Medical Reports"],
            
            writing_style=WritingStyle.EDUCATIONAL,
            tone_keywords=["伤病情况", "身体状态", "体能储备", "伤病史", "恢复情况"],
            signature_phrases=[
                "从医学角度分析",
                "伤病对比赛的影响",
                "球员身体状况",
                "体能和健康是基础",
                "伤病风险评估"
            ],
            
            analysis_priorities=[
                "Key player injury status",
                "Injury history patterns",
                "Recovery time analysis",
                "Squad depth assessment",
                "Physical condition trends"
            ],
            key_metrics=["Injury List", "Recovery Time", "Squad Availability", "Fatigue Index", "Medical History"],
            preferred_bet_types=["Match Result", "Player Props", "Team Total Goals"],
            
            win_rate=76.3,
            avg_return=1.22,
            total_predictions=341,
            successful_predictions=260,
            followers_count=9432,
            
            article_templates={
                "opening": "从医学和体能角度全面分析{home_team}对阵{away_team}。",
                "recent_form": "分析{team}球员近期的身体状况和伤病影响：",
                "historical": "回顾双方历史交锋中的伤病因素影响：",
                "prediction": "考虑伤病和体能因素，医学分析预测："
            },
            opening_templates=[
                "健康的球员才能踢出好比赛",
                "让我们从医学角度看足球",
                "身体是革命的本钱"
            ],
            conclusion_templates=[
                "关注球员健康，理性分析",
                "伤病信息很重要",
                "健康第一，比赛第二"
            ]
        )
        
        # 5. The Asian Handicap Master
        experts["handicap_master"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="代红",
            nickname="盘口专家",
            bio="Asian betting market specialist with deep understanding of handicap movements and Asian bookmaker psychology.",
            avatar_url="/avatars/handicap_master.png",
            
            primary_expertise=ExpertiseArea.ASIAN_HANDICAP,
            secondary_expertise=[ExpertiseArea.VALUE_BETTING, ExpertiseArea.PSYCHOLOGY],
            specializations=["Asian Handicap", "Market Movement", "Bookmaker Analysis", "Water Level", "Line Movement"],
            
            writing_style=WritingStyle.AUTHORITATIVE,
            tone_keywords=["亚盘分析", "盘口", "水位", "机构态度", "市场反应"],
            signature_phrases=[
                "亚盘开出",
                "盘口显示机构态度",
                "水位变化反映",
                "让球盘分析",
                "亚洲博彩公司"
            ],
            
            analysis_priorities=[
                "Initial handicap line",
                "Line movement patterns",
                "Water level changes",
                "Bookmaker behavior",
                "Market sentiment"
            ],
            key_metrics=["Opening Line", "Current Line", "Water Level", "Line Movement", "Closing Line"],
            preferred_bet_types=["Asian Handicap", "Level Ball", "Goal Line"],
            
            win_rate=79.1,
            avg_return=1.35,
            total_predictions=612,
            successful_predictions=484,
            followers_count=18765,
            
            article_templates={
                "opening": "深度解析{home_team} vs {away_team}的亚盘走势和机构态度。",
                "recent_form": "从亚盘角度分析{team}近期的市场表现：",
                "historical": "回顾双方交锋的历史盘口特征：",
                "prediction": "综合盘口分析和水位走势，亚盘预测："
            },
            opening_templates=[
                "亚盘是智慧的体现",
                "盘口背后的秘密",
                "让我们解读亚洲市场"
            ],
            conclusion_templates=[
                "跟随聪明钱的方向",
                "亚盘是最诚实的市场",
                "盘口胜过千言万语"
            ]
        )
        
        # 6. The Goal Prophet - Over/Under Specialist
        experts["goal_prophet"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="白羊",
            nickname="进球预言家",
            bio="Goal-focused analyst who specializes in predicting total goals, BTTS, and scoring patterns with remarkable accuracy.",
            avatar_url="/avatars/goal_prophet.png",
            
            primary_expertise=ExpertiseArea.GOALS,
            secondary_expertise=[ExpertiseArea.STATISTICS, ExpertiseArea.TACTICS],
            specializations=["Total Goals", "Both Teams to Score", "Goal Timing", "Scoring Patterns", "Clean Sheets"],
            
            writing_style=WritingStyle.PASSIONATE,
            tone_keywords=["进球", "火力", "攻击力", "防守", "进球模式"],
            signature_phrases=[
                "进球是足球的灵魂",
                "攻防平衡决定进球数",
                "大小球的奥秘",
                "双方都有得分能力",
                "进球时间分布"
            ],
            
            analysis_priorities=[
                "Average goals per game",
                "Scoring frequency",
                "Both teams to score rate",
                "Clean sheet percentage",
                "Goal timing patterns"
            ],
            key_metrics=["Goals Per Game", "BTTS Rate", "Clean Sheet %", "First Goal Time", "Goal Distribution"],
            preferred_bet_types=["Over/Under Goals", "Both Teams to Score", "Total Goals"],
            
            win_rate=73.7,
            avg_return=1.28,
            total_predictions=445,
            successful_predictions=328,
            followers_count=11234,
            
            article_templates={
                "opening": "聚焦进球，深度分析{home_team} vs {away_team}的得分潜力。",
                "recent_form": "分析{team}近期的进攻火力和防守表现：",
                "historical": "回顾双方历史交锋的进球特征：",
                "prediction": "基于进球模式和攻防分析，大小球预测："
            },
            opening_templates=[
                "进球让足球变得精彩",
                "让我们预测进球的盛宴",
                "攻守之间见真章"
            ],
            conclusion_templates=[
                "进球是王道",
                "攻防俱佳方能制胜",
                "相信火力，相信进球"
            ]
        )
        
        # 7. The Home Advantage Analyst
        experts["home_analyst"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="花芯",
            nickname="主场专家",
            bio="Specialist in home/away form analysis, crowd psychology, and venue-specific performance patterns.",
            avatar_url="/avatars/home_analyst.png",
            
            primary_expertise=ExpertiseArea.HOME_AWAY,
            secondary_expertise=[ExpertiseArea.PSYCHOLOGY, ExpertiseArea.CONDITIONS],
            specializations=["Home Advantage", "Away Form", "Venue Analysis", "Crowd Impact", "Travel Fatigue"],
            
            writing_style=WritingStyle.CONVERSATIONAL,
            tone_keywords=["主场", "客场", "主场优势", "客场表现", "主客场差异"],
            signature_phrases=[
                "主场优势不容忽视",
                "客场作战的挑战",
                "主客场表现差异",
                "主场球迷的力量",
                "熟悉的环境很重要"
            ],
            
            analysis_priorities=[
                "Home vs away performance",
                "Venue-specific records",
                "Crowd attendance impact",
                "Travel distance effects",
                "Home/away goal difference"
            ],
            key_metrics=["Home Win Rate", "Away Form", "Home Goals", "Away Goals", "Venue Record"],
            preferred_bet_types=["Match Result", "Asian Handicap", "Home/Away Goals"],
            
            win_rate=72.4,
            avg_return=1.19,
            total_predictions=378,
            successful_predictions=274,
            followers_count=8901,
            
            article_templates={
                "opening": "主客场因素深度分析：{home_team}主场迎战{away_team}。",
                "recent_form": "分析{team}的主客场表现特点：",
                "historical": "双方历史交锋中的主客场规律：",
                "prediction": "考虑主客场因素，本场比赛预测："
            },
            opening_templates=[
                "主场作战总有优势",
                "客场征战考验实力",
                "主客场表现见分晓"
            ],
            conclusion_templates=[
                "主场优势要重视",
                "主客场差异很关键",
                "熟悉环境助力发挥"
            ]
        )
        
        # 8. The Weather Watcher - Conditions Expert
        experts["weather_watcher"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="内幕爆析",
            nickname="天气专家",
            bio="Meteorological analyst who studies the impact of weather conditions, pitch conditions, and environmental factors on match outcomes.",
            avatar_url="/avatars/weather_watcher.png",
            
            primary_expertise=ExpertiseArea.CONDITIONS,
            secondary_expertise=[ExpertiseArea.TACTICS, ExpertiseArea.STATISTICS],
            specializations=["Weather Impact", "Pitch Conditions", "Temperature Effects", "Wind Analysis", "Rain Impact"],
            
            writing_style=WritingStyle.TECHNICAL,
            tone_keywords=["天气", "气候", "场地", "环境", "条件"],
            signature_phrases=[
                "天气条件对比赛的影响",
                "场地环境因素",
                "气候适应能力",
                "外部条件分析",
                "环境优势"
            ],
            
            analysis_priorities=[
                "Weather forecast impact",
                "Pitch condition assessment",
                "Temperature adaptation",
                "Wind direction effects",
                "Precipitation probability"
            ],
            key_metrics=["Temperature", "Humidity", "Wind Speed", "Precipitation", "Pitch Quality"],
            preferred_bet_types=["Over/Under Goals", "Both Teams to Score", "Match Result"],
            
            win_rate=70.5,
            avg_return=1.15,
            total_predictions=289,
            successful_predictions=204,
            followers_count=6789,
            
            article_templates={
                "opening": "天气和环境因素分析：{home_team} vs {away_team}比赛条件评估。",
                "recent_form": "分析{team}在不同天气条件下的表现：",
                "historical": "回顾双方在类似条件下的历史表现：",
                "prediction": "综合天气和环境因素，条件分析预测："
            },
            opening_templates=[
                "天时地利人和很重要",
                "环境因素不容忽视",
                "让我们关注比赛条件"
            ],
            conclusion_templates=[
                "适应环境者胜出",
                "天气是比赛的变数",
                "条件优势要利用"
            ]
        )
        
        # 9. The Mind Reader - Psychology Expert
        experts["mind_reader"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="赢盘王",
            nickname="心理专家",
            bio="Sports psychologist specializing in team motivation, pressure situations, and psychological factors in football performance.",
            avatar_url="/avatars/mind_reader.png",
            
            primary_expertise=ExpertiseArea.PSYCHOLOGY,
            secondary_expertise=[ExpertiseArea.HISTORICAL, ExpertiseArea.HOME_AWAY],
            specializations=["Team Psychology", "Pressure Situations", "Motivation Analysis", "Mental Strength", "Confidence Levels"],
            
            writing_style=WritingStyle.PASSIONATE,
            tone_keywords=["心理", "情绪", "信心", "压力", "动机"],
            signature_phrases=[
                "心理因素很关键",
                "情绪状态影响发挥",
                "信心是制胜法宝",
                "压力下的表现",
                "心理优势明显"
            ],
            
            analysis_priorities=[
                "Team morale assessment",
                "Pressure situation analysis",
                "Confidence level evaluation",
                "Motivational factors",
                "Mental resilience"
            ],
            key_metrics=["Morale Index", "Pressure Rating", "Confidence Level", "Mental Strength", "Motivation Score"],
            preferred_bet_types=["Match Result", "Double Chance", "Asian Handicap"],
            
            win_rate=75.6,
            avg_return=1.21,
            total_predictions=334,
            successful_predictions=252,
            followers_count=10876,
            
            article_templates={
                "opening": "心理层面深度解析{home_team}对阵{away_team}的精神状态。",
                "recent_form": "分析{team}近期的心理状态和情绪表现：",
                "historical": "回顾双方心理交锋的历史特征：",
                "prediction": "基于心理分析和精神状态，心理预测："
            },
            opening_templates=[
                "心理决定一切",
                "让我们走进球员内心",
                "精神力量不可小觑"
            ],
            conclusion_templates=[
                "心理强者笑到最后",
                "情绪管理很重要",
                "心态决定成败"
            ]
        )
        
        # 10. The Value Hunter - Value Betting Expert
        experts["value_hunter"] = ExpertProfile(
            id=str(uuid.uuid4()),
            name="鼎峰",
            nickname="价值猎手",
            bio="Professional bettor and value analyst who identifies mispriced odds and profitable betting opportunities with mathematical precision.",
            avatar_url="/avatars/value_hunter.png",
            
            primary_expertise=ExpertiseArea.VALUE_BETTING,
            secondary_expertise=[ExpertiseArea.STATISTICS, ExpertiseArea.ASIAN_HANDICAP],
            specializations=["Value Betting", "Odds Analysis", "Market Inefficiency", "Probability Assessment", "ROI Optimization"],
            
            writing_style=WritingStyle.MINIMALIST,
            tone_keywords=["价值", "赔率", "期望值", "盈利", "投资回报"],
            signature_phrases=[
                "寻找市场的错误定价",
                "价值就是利润",
                "数学期望值分析",
                "长期盈利的秘诀",
                "理性投资理念"
            ],
            
            analysis_priorities=[
                "Odds value assessment",
                "Market efficiency analysis",
                "Probability calculation",
                "Expected value computation",
                "Risk-reward evaluation"
            ],
            key_metrics=["True Odds", "Market Odds", "Value %", "Expected Value", "ROI"],
            preferred_bet_types=["Value Bets", "Arbitrage", "Asian Handicap"],
            
            win_rate=77.8,
            avg_return=1.42,
            total_predictions=567,
            successful_predictions=441,
            followers_count=14523,
            
            article_templates={
                "opening": "价值分析：{home_team} vs {away_team}的投资机会评估。",
                "recent_form": "从投资角度评估{team}的价值表现：",
                "historical": "历史数据中的价值发现规律：",
                "prediction": "基于价值分析和期望值计算，投资建议："
            },
            opening_templates=[
                "价值是永恒的追求",
                "让我们寻找市场机会",
                "理性投资，长期盈利"
            ],
            conclusion_templates=[
                "价值投资是王道",
                "耐心等待好机会",
                "数学不会骗人"
            ]
        )
        
        return experts
    
    def get_expert_by_id(self, expert_id: str) -> Optional[ExpertProfile]:
        """Get expert profile by ID"""
        for expert in self.experts.values():
            if expert.id == expert_id:
                return expert
        return None
    
    def get_expert_by_nickname(self, nickname: str) -> Optional[ExpertProfile]:
        """Get expert profile by nickname"""
        for expert in self.experts.values():
            if expert.nickname == nickname:
                return expert
        return None
    
    def get_experts_by_expertise(self, expertise: ExpertiseArea) -> List[ExpertProfile]:
        """Get all experts with specific primary expertise"""
        return [
            expert for expert in self.experts.values()
            if expert.primary_expertise == expertise
        ]
    
    def get_all_experts(self) -> List[ExpertProfile]:
        """Get all expert profiles"""
        return list(self.experts.values())
    
    def generate_expert_article(
        self, 
        expert_key: str, 
        match_info: Dict[str, Any],
        odds_info: Dict[str, Any],
        historical_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a specialized article based on expert's profile and expertise
        
        Args:
            expert_key: Key identifier for the expert
            match_info: Match information dictionary
            odds_info: Odds and betting information
            historical_data: Historical match data
            
        Returns:
            Complete article with expert's unique style and focus
        """
        if expert_key not in self.experts:
            raise ValueError(f"Expert {expert_key} not found")
            
        expert = self.experts[expert_key]
        
        # Generate article based on expert's specialty
        article = {
            "expert_info": {
                "name": expert.name,
                "nickname": expert.nickname,
                "expertise": expert.primary_expertise.value,
                "writing_style": expert.writing_style.value
            },
            "title": self._generate_specialized_title(expert, match_info),
            "opening": self._generate_opening(expert, match_info),
            "sections": self._generate_specialized_sections(expert, match_info, odds_info, historical_data),
            "prediction": self._generate_specialized_prediction(expert, match_info, odds_info),
            "conclusion": self._generate_conclusion(expert, match_info),
            "confidence": self._calculate_expert_confidence(expert, match_info),
            "betting_advice": self._generate_betting_advice(expert, odds_info)
        }
        
        return article
    
    def _generate_specialized_title(self, expert: ExpertProfile, match_info: Dict[str, Any]) -> str:
        """Generate title based on expert's specialty"""
        home_team = match_info.get("home_team", "主队")
        away_team = match_info.get("away_team", "客队")
        
        specialty_titles = {
            ExpertiseArea.STATISTICS: f"数据解析：{home_team} vs {away_team} 深度统计分析",
            ExpertiseArea.TACTICS: f"战术对决：{home_team} vs {away_team} 技战术剖析",
            ExpertiseArea.HISTORICAL: f"历史回望：{home_team} vs {away_team} 传统交锋解读",
            ExpertiseArea.INJURIES: f"伤病报告：{home_team} vs {away_team} 球员状态分析",
            ExpertiseArea.ASIAN_HANDICAP: f"亚盘解读：{home_team} vs {away_team} 盘口分析",
            ExpertiseArea.GOALS: f"进球预测：{home_team} vs {away_team} 攻防火力对比",
            ExpertiseArea.HOME_AWAY: f"主客分析：{home_team} vs {away_team} 主客场优势",
            ExpertiseArea.CONDITIONS: f"条件分析：{home_team} vs {away_team} 天气场地因素",
            ExpertiseArea.PSYCHOLOGY: f"心理解读：{home_team} vs {away_team} 精神状态对比",
            ExpertiseArea.VALUE_BETTING: f"价值发现：{home_team} vs {away_team} 投资机会分析"
        }
        
        return specialty_titles.get(expert.primary_expertise, f"{home_team} vs {away_team} 专业分析")
    
    def _generate_opening(self, expert: ExpertProfile, match_info: Dict[str, Any]) -> str:
        """Generate opening based on expert's style"""
        home_team = match_info.get("home_team", "主队")
        away_team = match_info.get("away_team", "客队")
        
        template = expert.article_templates.get("opening", "专业分析{home_team}对阵{away_team}。")
        opening = template.format(home_team=home_team, away_team=away_team)
        
        # Add expert's signature opening style
        if expert.opening_templates:
            import random
            signature_opening = random.choice(expert.opening_templates)
            opening = f"{signature_opening}。\n\n{opening}"
        
        return opening
    
    def _generate_specialized_sections(
        self, 
        expert: ExpertProfile, 
        match_info: Dict[str, Any],
        odds_info: Dict[str, Any],
        historical_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate sections based on expert's expertise"""
        sections = {}
        
        # All experts include basic sections but with their own focus
        sections["近期表现"] = self._generate_recent_form_section(expert, match_info)
        sections["历史交锋"] = self._generate_historical_section(expert, historical_data, match_info)
        sections["专业分析"] = self._generate_specialty_section(expert, match_info, odds_info, historical_data)
        sections["预测分析"] = self._generate_specialized_prediction(expert, match_info, odds_info)
        
        return sections
    
    def _generate_recent_form_section(self, expert: ExpertProfile, match_info: Dict[str, Any]) -> str:
        """Generate recent form section with expert's focus"""
        home_team = match_info.get("home_team", "主队")
        away_team = match_info.get("away_team", "客队")
        
        # Base recent form analysis with expert's perspective
        content = f"近期表现分析\n\n"
        
        # Add expert's specific focus
        if expert.primary_expertise == ExpertiseArea.STATISTICS:
            content += f"从数据角度分析，{home_team}近5场比赛的预期进球(xG)为2.1，实际进球2.3，转化率较高。\n"
            content += f"{away_team}近期防守表现稳定，场均失球1.2个，防守效率位居联赛前列。"
            
        elif expert.primary_expertise == ExpertiseArea.TACTICS:
            content += f"{home_team}近期战术执行出色，4-2-3-1阵型下中场控制力强，边路传中成功率达78%。\n"
            content += f"{away_team}采用5-3-2防守反击战术，反击成功率高，但控球率偏低。"
            
        elif expert.primary_expertise == ExpertiseArea.INJURIES:
            content += f"{home_team}主力阵容完整，核心球员身体状况良好，无重大伤病困扰。\n"
            content += f"{away_team}中场核心因伤缺阵，替补球员能力有限，影响战术执行。"
            
        elif expert.primary_expertise == ExpertiseArea.GOALS:
            content += f"{home_team}近期攻击火力强劲，场均进球2.4个，主场进球效率更高。\n"
            content += f"{away_team}防守端表现一般，场均失球1.8个，客场防守压力较大。"
            
        else:
            # Default recent form analysis
            content += f"{home_team}近期状态出色，近5场3胜1平1负，攻防两端表现均衡。\n"
            content += f"{away_team}客场表现一般，近5个客场2胜1平2负，状态起伏较大。"
        
        return content
    
    def _generate_historical_section(self, expert: ExpertProfile, historical_data: Dict[str, Any], match_info: Dict[str, Any]) -> str:
        """Generate historical section with expert's perspective"""
        home_team = match_info.get("home_team", "主队")
        away_team = match_info.get("away_team", "客队")
        
        content = f"历史交锋分析\n\n"
        
        if expert.primary_expertise == ExpertiseArea.HISTORICAL:
            content += f"深入历史档案，{home_team}与{away_team}过去10次交锋中，主队6胜2平2负占据明显优势。\n"
            content += f"从时间维度看，双方最近3次交锋均产生3球以上，场面较为开放。\n"
            content += f"值得注意的是，{away_team}近年来在{home_team}主场从未获胜，心理层面处于劣势。"
            
        elif expert.primary_expertise == ExpertiseArea.PSYCHOLOGY:
            content += f"心理层面分析，{home_team}在主场面对{away_team}时信心充足，历史优势带来心理优势。\n"
            content += f"{away_team}客场挑战{home_team}时往往保守，缺乏必胜信念，影响临场发挥。"
            
        elif expert.primary_expertise == ExpertiseArea.GOALS:
            content += f"进球数据显示，双方历史交锋场均进球2.8个，大球概率较高。\n"
            content += f"{home_team}主场面对{away_team}场均进球2.1个，客队场均失球1.7个。"
            
        else:
            # Standard historical analysis
            content += f"历史交锋记录显示，{home_team}与{away_team}近期交锋较为激烈。\n"
            content += f"过去5次交锋，主队3胜1平1负，主场优势明显。"
            
        return content
    
    def _generate_specialty_section(
        self, 
        expert: ExpertProfile, 
        match_info: Dict[str, Any],
        odds_info: Dict[str, Any],
        historical_data: Dict[str, Any]
    ) -> str:
        """Generate the expert's specialty analysis section"""
        specialty_content = {
            ExpertiseArea.STATISTICS: self._generate_stats_analysis(match_info, odds_info),
            ExpertiseArea.TACTICS: self._generate_tactical_analysis(match_info),
            ExpertiseArea.HISTORICAL: self._generate_historical_analysis(historical_data, match_info),
            ExpertiseArea.INJURIES: self._generate_injury_analysis(match_info),
            ExpertiseArea.ASIAN_HANDICAP: self._generate_handicap_analysis(odds_info, match_info),
            ExpertiseArea.GOALS: self._generate_goals_analysis(match_info, odds_info),
            ExpertiseArea.HOME_AWAY: self._generate_home_away_analysis(match_info),
            ExpertiseArea.CONDITIONS: self._generate_conditions_analysis(match_info),
            ExpertiseArea.PSYCHOLOGY: self._generate_psychology_analysis(match_info),
            ExpertiseArea.VALUE_BETTING: self._generate_value_analysis(odds_info, match_info)
        }
        
        return specialty_content.get(expert.primary_expertise, "专业分析内容")
    
    def _generate_stats_analysis(self, match_info: Dict[str, Any], odds_info: Dict[str, Any]) -> str:
        """Generate statistical analysis"""
        return """高级数据分析

通过机器学习模型分析，本场比赛的关键指标如下：
- 预期进球(xG)：主队2.3 vs 客队1.7
- 射门转化率：主队13.2% vs 客队11.8%
- 控球率预测：主队58% vs 客队42%
- 关键传球成功率：主队82% vs 客队76%

基于泊松分布模型，本场比赛最可能的比分为2-1或1-1。"""
    
    def _generate_tactical_analysis(self, match_info: Dict[str, Any]) -> str:
        """Generate tactical analysis"""
        return """战术层面分析

主队预计采用4-3-3阵型，高位压迫，通过边路快速推进制造威胁。
客队可能采用5-4-1防守反击，利用快速反击寻找机会。

关键战术对决：
1. 主队边锋 vs 客队边后卫的一对一较量
2. 中场控制权争夺将决定比赛节奏
3. 定位球将是重要的得分机会

预计主队主导比赛，但客队反击威胁不容小觑。"""
    
    def _generate_historical_analysis(self, historical_data: Dict[str, Any], match_info: Dict[str, Any]) -> str:
        """Generate historical pattern analysis"""
        return """历史规律深度解析

通过对历史数据的深度挖掘，发现以下规律：
1. 双方近10年交锋，春季比赛主队胜率更高
2. 雨天条件下，防守型球队优势明显
3. 赛季末期，主队主场优势会放大

本赛季同期对比：
- 主队主场战绩优于去年同期
- 客队客场表现与历史平均水平持平

历史告诉我们，相似条件下主队获胜概率为65%。"""
    
    def _generate_injury_analysis(self, match_info: Dict[str, Any]) -> str:
        """Generate injury impact analysis"""
        return """伤病情况医学评估

主队伤病情况：
- 主力前锋轻微肌肉疲劳，预计能够首发
- 中后卫脚踝扭伤已恢复，不影响比赛
- 整体健康状况良好，体能储备充足

客队伤病情况：
- 核心中场膝盖伤势未愈，确认缺席
- 替补门将肩膀不适，出场存疑
- 球队整体疲劳度较高，轮换可能性大

伤病因素分析：客队核心缺阵将显著影响中场创造力。"""
    
    def _generate_handicap_analysis(self, odds_info: Dict[str, Any], match_info: Dict[str, Any]) -> str:
        """Generate Asian handicap analysis"""
        return """亚洲盘口深度解读

初盘分析：
- 主队让球0.5球，水位0.95/0.85
- 机构对主队略显信心，但不敢深让

盘口走势：
- 开盘后主队水位从0.90升至0.95
- 客队水位相应下调，资金流向平衡

机构态度：
- 亚洲主流机构普遍看好主队不败
- 欧洲机构对比赛结果相对谨慎

推荐：主队-0.5球 中等信心投注"""
    
    def _generate_goals_analysis(self, match_info: Dict[str, Any], odds_info: Dict[str, Any]) -> str:
        """Generate goals analysis"""
        return """进球数据专业分析

攻击火力对比：
- 主队场均进球2.1个，主场攻击力更强
- 客队场均进球1.6个，客场进攻乏力

防守强度评估：
- 主队场均失球1.3个，主场防守稳固
- 客队场均失球1.8个，客场防守脆弱

大小球分析：
- 历史交锋大球率70%
- 双方近期比赛大球趋势明显
- 预测总进球数：2.5-3.5球

推荐：大2.5球 高信心投注"""
    
    def _generate_home_away_analysis(self, match_info: Dict[str, Any]) -> str:
        """Generate home/away form analysis"""
        return """主客场表现对比分析

主队主场优势：
- 主场14战10胜2平2负，胜率71.4%
- 主场场均进球2.3个，失球1.1个
- 主场观众平均上座率85%，氛围热烈

客队客场表现：
- 客场15战5胜3平7负，胜率33.3%
- 客场场均进球1.4个，失球2.0个
- 长途旅行影响，体能消耗较大

主客场差异：
主队主客场表现差异不大，实力稳定
客队主客场差异明显，客场竞争力下降

结论：主场因素将成为比赛的决定性因素"""
    
    def _generate_conditions_analysis(self, match_info: Dict[str, Any]) -> str:
        """Generate weather/conditions analysis"""
        return """比赛条件环境分析

天气预报：
- 比赛日气温15-18°C，适宜足球比赛
- 降雨概率20%，基本无影响
- 风力2-3级，对传球影响较小

场地条件：
- 草皮质量优良，利于技术发挥
- 场地排水系统完善，无积水风险
- 照明条件excellent，视线清晰

环境影响评估：
- 温和天气条件有利于技术型球队
- 良好场地条件利于流畅比赛
- 整体环境对双方相对公平

预测：天气条件不会成为胜负关键因素"""
    
    def _generate_psychology_analysis(self, match_info: Dict[str, Any]) -> str:
        """Generate psychological analysis"""
        return """心理因素深度剖析

主队心理状态：
- 近期连胜增强信心，士气高涨
- 主场作战压力相对较小
- 球员求胜欲望强烈，比赛动机充足

客队心理状态：
- 客场连败影响信心，心理包袱重
- 面对强队时容易产生畏惧心理
- 保级压力下求分心切，可能影响发挥

心理优势对比：
- 主队在心理层面占据明显优势
- 历史交锋记录增强主队信心
- 客队需要克服心理障碍才能发挥实力

心理预测：主队心理优势将转化为场上优势"""
    
    def _generate_value_analysis(self, odds_info: Dict[str, Any], match_info: Dict[str, Any]) -> str:
        """Generate value betting analysis"""
        return """价值投注机会分析

赔率评估：
- 主胜赔率2.10，隐含概率47.6%
- 平局赔率3.40，隐含概率29.4%
- 客胜赔率3.20，隐含概率31.3%

真实概率计算：
- 主胜真实概率：55%（价值+7.4%）
- 平局真实概率：25%（价值-4.4%）
- 客胜真实概率：20%（价值-11.3%）

价值投注机会：
✓ 主胜存在显著价值，推荐投注
✗ 平局和客胜赔率偏低，不建议投注

期望值计算：
主胜投注期望回报率：+15.5%
建议投注：主胜 高信心3单位"""
    
    def _generate_specialized_prediction(self, expert: ExpertProfile, match_info: Dict[str, Any], odds_info: Dict[str, Any]) -> str:
        """Generate prediction with expert's style"""
        predictions = {
            ExpertiseArea.STATISTICS: "基于数学模型，预测比分2-1，主胜概率68%",
            ExpertiseArea.TACTICS: "战术分析显示主队优势明显，预测2-0或1-0小胜",
            ExpertiseArea.HISTORICAL: "历史经验告诉我们，主队将延续主场不败，预测1-1或2-1",
            ExpertiseArea.INJURIES: "考虑伤病影响，主队人员完整优势突出，预测2-1胜出",
            ExpertiseArea.ASIAN_HANDICAP: "亚盘-0.5球有价值，推荐主队小胜1-0或2-1",
            ExpertiseArea.GOALS: "双方攻击力强，预测大比分3-1或2-2，大球稳胆",
            ExpertiseArea.HOME_AWAY: "主场优势决定性，主队必胜，预测2-0或3-1",
            ExpertiseArea.CONDITIONS: "天气条件完美，技术发挥充分，预测2-1精彩对决",
            ExpertiseArea.PSYCHOLOGY: "主队心理优势巨大，客队必败，预测3-0大胜",
            ExpertiseArea.VALUE_BETTING: "价值在主胜，期望回报15.5%，推荐2-1结果"
        }
        
        return predictions.get(expert.primary_expertise, "综合分析预测主队2-1获胜")
    
    def _generate_conclusion(self, expert: ExpertProfile, match_info: Dict[str, Any]) -> str:
        """Generate conclusion with expert's signature style"""
        if expert.conclusion_templates:
            import random
            signature = random.choice(expert.conclusion_templates)
            return f"{signature}。让我们拭目以待这场精彩对决的结果。"
        
        return "综合所有分析因素，我们对本场比赛充满期待。"
    
    def _calculate_expert_confidence(self, expert: ExpertProfile, match_info: Dict[str, Any]) -> int:
        """Calculate expert's confidence based on their specialty"""
        base_confidence = 75
        
        # Adjust based on expertise area
        confidence_modifiers = {
            ExpertiseArea.STATISTICS: 5,  # Data-driven, higher confidence
            ExpertiseArea.VALUE_BETTING: 8,  # Mathematical precision
            ExpertiseArea.ASIAN_HANDICAP: 6,  # Market analysis
            ExpertiseArea.HISTORICAL: 3,  # Pattern-based
            ExpertiseArea.TACTICS: 4,  # Professional insight
            ExpertiseArea.INJURIES: 7,  # Clear impact assessment
            ExpertiseArea.GOALS: 2,  # More volatile
            ExpertiseArea.HOME_AWAY: 5,  # Clear patterns
            ExpertiseArea.CONDITIONS: 1,  # Weather is unpredictable
            ExpertiseArea.PSYCHOLOGY: 3   # Subjective analysis
        }
        
        modifier = confidence_modifiers.get(expert.primary_expertise, 0)
        return min(95, base_confidence + modifier)  # Cap at 95%
    
    def _generate_betting_advice(self, expert: ExpertProfile, odds_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate betting advice based on expert's specialty"""
        advice_templates = {
            ExpertiseArea.STATISTICS: {
                "primary_bet": "主胜",
                "stake": "2单位",
                "reasoning": "数据模型显示主队优势明显",
                "secondary_bets": ["大2.5球", "主队-0.5球"]
            },
            ExpertiseArea.ASIAN_HANDICAP: {
                "primary_bet": "主队-0.5球",
                "stake": "3单位",
                "reasoning": "亚盘水位变化显示机构态度",
                "secondary_bets": ["主队不败", "让球大小球组合"]
            },
            ExpertiseArea.GOALS: {
                "primary_bet": "大2.5球",
                "stake": "2单位",
                "reasoning": "双方攻击火力分析支持大球",
                "secondary_bets": ["双方进球", "总进球3-4个"]
            },
            ExpertiseArea.VALUE_BETTING: {
                "primary_bet": "主胜",
                "stake": "3单位",
                "reasoning": "期望值15.5%，价值显著",
                "secondary_bets": ["主胜+大2.5球", "主队-0.5球"]
            }
        }
        
        default_advice = {
            "primary_bet": "主队不败",
            "stake": "1单位", 
            "reasoning": "综合分析支持主队优势",
            "secondary_bets": ["平局保险", "小球"]
        }
        
        return advice_templates.get(expert.primary_expertise, default_advice)


# Singleton instance for easy access
prediction_experts = PredictionExpertProfiles()

# Export for external use
__all__ = [
    'ExpertiseArea',
    'WritingStyle', 
    'ExpertProfile',
    'PredictionExpertProfiles',
    'prediction_experts'
]