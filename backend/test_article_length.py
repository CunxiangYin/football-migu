#!/usr/bin/env python
"""测试预测文章生成的字数"""

from agents.football_prediction_writer import FootballPredictionWriter, TeamInfo, MatchInfo, OddsInfo, HistoricalData
import json

# 创建测试数据
home_team = TeamInfo(
    name='东京FC',
    recent_form=['W', 'W', 'D', 'L', 'W'],
    league_position=3,
    home_away_record='主场5胜2平1负',
    key_players_status={},
    recent_performance='近5场3胜1平1负，进11球失5球，主场表现强势，进攻火力十足，防守稳固。最近一场主场比赛3-0大胜对手，球队士气高涨。'
)

away_team = TeamInfo(
    name='京都不死鸟',
    recent_form=['L', 'D', 'W', 'W', 'L'],
    league_position=7,
    home_away_record='客场2胜2平4负',
    key_players_status={'山田太郎': '伤缺', '铃木一郎': '状态不佳'},
    recent_performance='近5场2胜1平2负，进7球失9球，客场表现不稳定，防守存在明显漏洞。上轮客场1-3惨败，暴露出防线问题。'
)

match_info = MatchInfo(
    home_team=home_team,
    away_team=away_team,
    league='J联赛',
    match_time='2025-09-05 18:00',
    venue='东京体育场',
    weather='晴，25℃'
)

odds_info = OddsInfo(
    home_win=1.85,
    draw=3.40,
    away_win=4.20,
    asian_handicap='主队-0.5',
    over_under='2.5球'
)

historical_data = HistoricalData(
    h2h_results=[
        {'winner': 'home', 'score': '2-1'},
        {'winner': 'draw', 'score': '1-1'},
        {'winner': 'home', 'score': '3-0'},
        {'winner': 'away', 'score': '0-1'},
        {'winner': 'home', 'score': '2-0'}
    ],
    home_team_home_record='主队主场对阵客队4胜1平1负，场均进2.3球失0.8球，优势明显',
    away_team_away_record='客队客场对阵主队1胜1平4负，场均进0.7球失2.0球，战绩不佳'
)

# 生成预测
writer = FootballPredictionWriter()
prediction = writer.generate_prediction(
    match_info=match_info,
    odds_info=odds_info,
    historical_data=historical_data,
    expert_confidence=85,
    api_predictions={'AI预测': '主队胜', '大数据分析': '2-1或3-1'}
)

# 输出完整文章
article = prediction['full_article']
print('=== 生成的预测文章 ===')
print(article)
print()
print(f'文章总字数: {len(article)} 字符')
print(f'不含空格和换行的字数: {len(article.replace(" ", "").replace("\\n", ""))} 字符')

# 统计中文字数
chinese_chars = 0
for char in article:
    if '\u4e00' <= char <= '\u9fff':
        chinese_chars += 1
print(f'中文字数: {chinese_chars} 个')

print()
print('=== 各部分字数统计 ===')
for section_name, section_content in prediction['sections'].items():
    chinese_count = sum(1 for char in section_content if '\u4e00' <= char <= '\u9fff')
    print(f'{section_name}: {len(section_content)} 字符 (中文: {chinese_count} 字)')
    
print()
print('=== 文章内容长度分析 ===')
lines = article.split('\n')
print(f'总行数: {len(lines)}')
print(f'平均每行字数: {len(article) // len(lines) if lines else 0} 字符')