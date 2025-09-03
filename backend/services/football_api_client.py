"""
Football API Client
用于从 API-Sports 获取足球数据
"""

import os
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class TeamStats:
    """球队统计数据"""
    team_id: int
    team_name: str
    league_position: int
    recent_form: str  # 最近5场比赛结果 WWDLL
    goals_for: int
    goals_against: int
    home_record: Dict[str, int]  # {"wins": 5, "draws": 2, "losses": 1}
    away_record: Dict[str, int]
    last_5_matches: List[Dict]

@dataclass
class H2HData:
    """历史交锋数据"""
    total_matches: int
    home_wins: int
    draws: int
    away_wins: int
    recent_matches: List[Dict]  # 最近5场交锋记录

class FootballAPIClient:
    """
    Football API 客户端
    使用 API-Sports 提供的足球数据
    """
    
    # League IDs from API-Sports
    LEAGUE_IDS = {
        "k_league_1": 292,  # 韩国K联赛1
        "j_league_1": 98,   # 日本J联赛1
    }
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('FOOTBALL_API_KEY')
        if not self.api_key:
            raise ValueError("FOOTBALL_API_KEY not provided")
            
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('errors'):
                logger.error(f"API Error: {data['errors']}")
                return None
                
            return data.get('response', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
            
    def get_team_statistics(self, team_id: int, league_id: int, season: int = None) -> TeamStats:
        """
        获取球队统计数据
        
        Args:
            team_id: 球队ID
            league_id: 联赛ID
            season: 赛季年份（默认当前赛季）
        """
        if not season:
            season = datetime.now().year
            
        # 获取球队基本信息和联赛排名
        standings_data = self._make_request(
            "/standings",
            params={"league": league_id, "season": season}
        )
        
        # 获取球队最近比赛
        fixtures_data = self._make_request(
            "/fixtures",
            params={"team": team_id, "last": 5, "status": "FT"}
        )
        
        # 获取球队统计
        stats_data = self._make_request(
            "/teams/statistics",
            params={"team": team_id, "league": league_id, "season": season}
        )
        
        if not all([standings_data, fixtures_data, stats_data]):
            return None
            
        # 解析数据
        team_stats = self._parse_team_stats(
            standings_data, fixtures_data, stats_data, team_id
        )
        
        return team_stats
        
    def _parse_team_stats(
        self, 
        standings: List,
        fixtures: List,
        stats: Dict,
        team_id: int
    ) -> TeamStats:
        """解析球队统计数据"""
        
        # 从积分榜获取排名和基本数据
        team_standing = None
        if standings and standings[0].get('league'):
            for group in standings[0]['league']['standings']:
                for team in group:
                    if team['team']['id'] == team_id:
                        team_standing = team
                        break
                        
        if not team_standing:
            return None
            
        # 解析最近5场比赛
        recent_form = team_standing.get('form', '')
        last_5_matches = []
        
        for fixture in fixtures[:5]:
            match_data = {
                'date': fixture['fixture']['date'],
                'home_team': fixture['teams']['home']['name'],
                'away_team': fixture['teams']['away']['name'],
                'score': f"{fixture['goals']['home']}-{fixture['goals']['away']}",
                'venue': fixture['fixture']['venue']['name']
            }
            last_5_matches.append(match_data)
            
        # 解析主客场战绩
        home_record = {
            'wins': team_standing.get('home', {}).get('win', 0),
            'draws': team_standing.get('home', {}).get('draw', 0),
            'losses': team_standing.get('home', {}).get('lose', 0)
        }
        
        away_record = {
            'wins': team_standing.get('away', {}).get('win', 0),
            'draws': team_standing.get('away', {}).get('draw', 0),
            'losses': team_standing.get('away', {}).get('lose', 0)
        }
        
        return TeamStats(
            team_id=team_id,
            team_name=team_standing['team']['name'],
            league_position=team_standing['rank'],
            recent_form=recent_form,
            goals_for=team_standing['all']['goals']['for'],
            goals_against=team_standing['all']['goals']['against'],
            home_record=home_record,
            away_record=away_record,
            last_5_matches=last_5_matches
        )
        
    def get_h2h_data(self, team1_id: int, team2_id: int, last: int = 5) -> H2HData:
        """
        获取两队历史交锋数据
        
        Args:
            team1_id: 球队1的ID
            team2_id: 球队2的ID
            last: 获取最近几场交锋（默认5场）
        """
        h2h_data = self._make_request(
            "/fixtures/headtohead",
            params={"h2h": f"{team1_id}-{team2_id}", "last": last}
        )
        
        if not h2h_data:
            return None
            
        return self._parse_h2h_data(h2h_data, team1_id, team2_id)
        
    def _parse_h2h_data(self, fixtures: List, team1_id: int, team2_id: int) -> H2HData:
        """解析历史交锋数据"""
        
        total_matches = len(fixtures)
        team1_wins = 0
        draws = 0
        team2_wins = 0
        recent_matches = []
        
        for fixture in fixtures:
            home_team = fixture['teams']['home']
            away_team = fixture['teams']['away']
            home_goals = fixture['goals']['home']
            away_goals = fixture['goals']['away']
            
            # 统计胜负
            if home_goals > away_goals:
                if home_team['id'] == team1_id:
                    team1_wins += 1
                else:
                    team2_wins += 1
            elif home_goals < away_goals:
                if away_team['id'] == team1_id:
                    team1_wins += 1
                else:
                    team2_wins += 1
            else:
                draws += 1
                
            # 记录比赛详情
            recent_matches.append({
                'date': fixture['fixture']['date'],
                'home_team': home_team['name'],
                'away_team': away_team['name'],
                'score': f"{home_goals}-{away_goals}",
                'venue': fixture['fixture']['venue']['name']
            })
            
        return H2HData(
            total_matches=total_matches,
            home_wins=team1_wins,
            draws=draws,
            away_wins=team2_wins,
            recent_matches=recent_matches
        )
        
    def get_fixtures_by_date_and_league(self, date: str, league_ids: List[int] = None) -> List[Dict]:
        """
        获取指定日期和联赛的比赛
        
        Args:
            date: 日期 (YYYY-MM-DD格式)
            league_ids: 联赛ID列表，默认为K联赛和J联赛
        """
        if league_ids is None:
            league_ids = [self.LEAGUE_IDS["k_league_1"], self.LEAGUE_IDS["j_league_1"]]
        
        all_fixtures = []
        for league_id in league_ids:
            fixtures = self._make_request(
                "/fixtures",
                params={
                    "date": date,
                    "league": league_id,
                    "season": datetime.now().year
                }
            )
            
            if fixtures:
                for fixture in fixtures:
                    all_fixtures.append(self._parse_fixture(fixture))
        
        return all_fixtures
    
    def get_today_tomorrow_matches(self) -> Dict[str, List[Dict]]:
        """
        获取今天和明天的K联赛、J联赛比赛
        """
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        return {
            "today": self.get_fixtures_by_date_and_league(today),
            "tomorrow": self.get_fixtures_by_date_and_league(tomorrow)
        }
    
    def get_upcoming_match(self, team1_id: int, team2_id: int) -> Dict:
        """
        获取即将进行的比赛信息
        
        Args:
            team1_id: 球队1的ID
            team2_id: 球队2的ID
        """
        # 获取未来比赛
        fixtures = self._make_request(
            "/fixtures",
            params={
                "team": team1_id,
                "next": 10,
                "status": "NS"  # Not Started
            }
        )
        
        if not fixtures:
            return None
            
        # 找到两队的对战
        for fixture in fixtures:
            if (fixture['teams']['home']['id'] == team2_id or 
                fixture['teams']['away']['id'] == team2_id):
                return self._parse_fixture(fixture)
                
        return None
        
    def _parse_fixture(self, fixture: Dict) -> Dict:
        """解析比赛信息"""
        return {
            'fixture_id': fixture['fixture']['id'],
            'date': fixture['fixture']['date'],
            'venue': fixture['fixture']['venue']['name'],
            'referee': fixture['fixture']['referee'],
            'home_team': {
                'id': fixture['teams']['home']['id'],
                'name': fixture['teams']['home']['name'],
                'logo': fixture['teams']['home']['logo']
            },
            'away_team': {
                'id': fixture['teams']['away']['id'],
                'name': fixture['teams']['away']['name'],
                'logo': fixture['teams']['away']['logo']
            },
            'league': {
                'id': fixture['league']['id'],
                'name': fixture['league']['name'],
                'country': fixture['league']['country']
            }
        }
        
    def get_team_injuries(self, team_id: int) -> List[Dict]:
        """
        获取球队伤病信息
        
        Args:
            team_id: 球队ID
        """
        injuries = self._make_request(
            "/injuries",
            params={"team": team_id, "current": "true"}
        )
        
        if not injuries:
            return []
            
        return [{
            'player': injury['player']['name'],
            'type': injury['player']['type'],
            'reason': injury['player']['reason'],
            'return_date': injury['player']['date']
        } for injury in injuries]
        
    def get_live_odds(self, fixture_id: int) -> Dict:
        """
        获取实时赔率
        
        Args:
            fixture_id: 比赛ID
        """
        odds = self._make_request(
            "/odds",
            params={"fixture": fixture_id}
        )
        
        if not odds or not odds[0].get('bookmakers'):
            return None
            
        # 解析第一个博彩公司的赔率
        bookmaker = odds[0]['bookmakers'][0]
        bets = bookmaker.get('bets', [])
        
        odds_data = {}
        for bet in bets:
            if bet['name'] == 'Match Winner':
                for value in bet['values']:
                    if value['value'] == 'Home':
                        odds_data['home_win'] = float(value['odd'])
                    elif value['value'] == 'Draw':
                        odds_data['draw'] = float(value['odd'])
                    elif value['value'] == 'Away':
                        odds_data['away_win'] = float(value['odd'])
                        
            elif bet['name'] == 'Asian Handicap':
                odds_data['asian_handicap'] = bet['values'][0] if bet['values'] else None
                
            elif bet['name'] == 'Total':
                odds_data['over_under'] = bet['values'][0] if bet['values'] else None
                
        return odds_data


class FootballDataAggregator:
    """
    足球数据聚合器
    整合API数据用于预测文章生成
    """
    
    def __init__(self, api_client: FootballAPIClient = None):
        self.api_client = api_client or FootballAPIClient()
        
    def prepare_prediction_data(
        self, 
        home_team_id: int,
        away_team_id: int,
        league_id: int,
        fixture_id: int = None
    ) -> Dict:
        """
        准备预测所需的所有数据
        
        Returns:
            包含所有预测所需数据的字典
        """
        
        # 获取两队统计数据
        home_stats = self.api_client.get_team_statistics(home_team_id, league_id)
        away_stats = self.api_client.get_team_statistics(away_team_id, league_id)
        
        # 获取历史交锋
        h2h = self.api_client.get_h2h_data(home_team_id, away_team_id)
        
        # 获取伤病信息
        home_injuries = self.api_client.get_team_injuries(home_team_id)
        away_injuries = self.api_client.get_team_injuries(away_team_id)
        
        # 获取赔率（如果有比赛ID）
        odds = None
        if fixture_id:
            odds = self.api_client.get_live_odds(fixture_id)
            
        # 构建数据结构
        prediction_data = {
            'home_team': {
                'name': home_stats.team_name if home_stats else 'Unknown',
                'recent_form': list(home_stats.recent_form) if home_stats else [],
                'league_position': home_stats.league_position if home_stats else 0,
                'home_away_record': f"主场{home_stats.home_record['wins']}胜{home_stats.home_record['draws']}平{home_stats.home_record['losses']}负" if home_stats else "",
                'key_players_status': {injury['player']: injury['reason'] for injury in home_injuries},
                'recent_performance': self._describe_recent_form(home_stats) if home_stats else ""
            },
            'away_team': {
                'name': away_stats.team_name if away_stats else 'Unknown',
                'recent_form': list(away_stats.recent_form) if away_stats else [],
                'league_position': away_stats.league_position if away_stats else 0,
                'home_away_record': f"客场{away_stats.away_record['wins']}胜{away_stats.away_record['draws']}平{away_stats.away_record['losses']}负" if away_stats else "",
                'key_players_status': {injury['player']: injury['reason'] for injury in away_injuries},
                'recent_performance': self._describe_recent_form(away_stats) if away_stats else ""
            },
            'historical_data': {
                'h2h_results': h2h.recent_matches if h2h else [],
                'home_team_home_record': f"主场对{away_stats.team_name if away_stats else '对手'}{h2h.home_wins if h2h else 0}胜{h2h.draws if h2h else 0}平{h2h.away_wins if h2h else 0}负",
                'away_team_away_record': f"客场对{home_stats.team_name if home_stats else '对手'}历史战绩"
            },
            'odds_info': odds if odds else {
                'home_win': 2.20,
                'draw': 3.30,
                'away_win': 2.80,
                'asian_handicap': '主队-0.5',
                'over_under': '2.5'
            }
        }
        
        return prediction_data
        
    def _describe_recent_form(self, stats: TeamStats) -> str:
        """描述球队近期表现"""
        if not stats:
            return "近期表现未知"
            
        wins = stats.recent_form.count('W')
        draws = stats.recent_form.count('D')
        losses = stats.recent_form.count('L')
        
        return f"近5场{wins}胜{draws}平{losses}负，{'状态出色' if wins >= 3 else '状态一般' if wins >= 2 else '状态低迷'}"


# 使用示例
if __name__ == "__main__":
    # 设置API密钥
    api_key = "91e2647e3d88e2b4340eeb841181413c"
    
    # 创建客户端
    client = FootballAPIClient(api_key)
    
    # 示例：获取曼联vs曼城的数据
    # 注意：需要实际的球队ID和联赛ID
    aggregator = FootballDataAggregator(client)
    
    # 准备预测数据
    # data = aggregator.prepare_prediction_data(
    #     home_team_id=33,  # 曼联
    #     away_team_id=50,  # 曼城
    #     league_id=39,     # 英超
    # )
    
    # print(json.dumps(data, ensure_ascii=False, indent=2))