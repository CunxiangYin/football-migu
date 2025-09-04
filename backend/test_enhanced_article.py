#!/usr/bin/env python
"""测试增强版预测文章生成的字数（1000-1500字）"""

from agents.enhanced_football_writer import EnhancedFootballWriter, TeamInfo, MatchInfo, OddsInfo, HistoricalData

# 创建测试数据
home_team = TeamInfo(
    name='东京FC',
    recent_form=['W', 'W', 'D', 'L', 'W'],
    league_position=3,
    home_away_record='主场8胜3平2负',
    key_players_status={},
    recent_performance='近5场3胜1平1负，进11球失5球，状态出色',
    goals_scored=11,
    goals_conceded=5,
    top_scorer='田中将大',
    formation='4-3-3'
)

away_team = TeamInfo(
    name='京都不死鸟',
    recent_form=['L', 'D', 'W', 'W', 'L'],
    league_position=7,
    home_away_record='客场3胜3平6负',
    key_players_status={'山田太郎': '膝伤缺阵', '铃木一郎': '轻伤可能出场'},
    recent_performance='近5场2胜1平2负，进7球失9球，防守问题明显',
    goals_scored=7,
    goals_conceded=9,
    top_scorer='佐藤健',
    formation='4-5-1'
)

match_info = MatchInfo(
    home_team=home_team,
    away_team=away_team,
    league='J联赛',
    match_time='2025-09-05 18:00',
    venue='东京国立竞技场',
    weather='晴，25℃，微风',
    referee='山本裁判',
    importance='常规赛第28轮'
)

odds_info = OddsInfo(
    home_win=1.85,
    draw=3.40,
    away_win=4.20,
    asian_handicap='主队-0.5',
    over_under='2.5球',
    odds_trend='主队赔率略有下降'
)

historical_data = HistoricalData(
    h2h_results=[
        {'winner': 'home', 'score': '2-1'},
        {'winner': 'draw', 'score': '1-1'},
        {'winner': 'home', 'score': '3-0'},
        {'winner': 'away', 'score': '0-1'},
        {'winner': 'home', 'score': '2-0'},
        {'winner': 'home', 'score': '4-2'},
        {'winner': 'draw', 'score': '2-2'},
        {'winner': 'home', 'score': '1-0'},
        {'winner': 'away', 'score': '1-3'},
        {'winner': 'home', 'score': '2-1'}
    ],
    home_team_home_record='主队主场对阵客队6胜1平2负，场均进2.4球失1.1球',
    away_team_away_record='客队客场对阵主队2胜1平6负，场均进1.0球失2.3球',
    last_meeting_details='上次交锋在3个月前，东京FC主场2-1击败京都不死鸟，田中将大梅开二度'
)

# 生成预测
writer = EnhancedFootballWriter()
prediction = writer.generate_prediction(
    match_info=match_info,
    odds_info=odds_info,
    historical_data=historical_data,
    expert_confidence=85,
    api_predictions={
        'AI预测系统': '主队胜，概率68%',
        '大数据模型': '预测比分2-1或3-1',
        '专家共识': '主队让球胜'
    }
)

# 输出完整文章
article = prediction['full_article']
print('='*60)
print('增强版预测文章（目标：1000-1500字）')
print('='*60)
print(article)
print()
print('='*60)
print('文章统计信息')
print('='*60)
print(f'总字符数: {len(article)} 个')
print(f'不含空格和换行: {len(article.replace(" ", "").replace("\\n", ""))} 个')

# 统计中文字数
chinese_chars = 0
for char in article:
    if '\u4e00' <= char <= '\u9fff':
        chinese_chars += 1
print(f'中文字数: {chinese_chars} 个')

# 统计英文单词
import re
english_words = len(re.findall(r'[a-zA-Z]+', article))
print(f'英文单词: {english_words} 个')

print()
print('各章节字数统计:')
print('-'*40)
for section_name, section_content in prediction['sections'].items():
    chinese_count = sum(1 for char in section_content if '\u4e00' <= char <= '\u9fff')
    total_chars = len(section_content)
    print(f'{section_name:10} | 总字符: {total_chars:4} | 中文: {chinese_count:4}')

print()
print('文章结构分析:')
print('-'*40)
lines = article.split('\n')
non_empty_lines = [line for line in lines if line.strip()]
print(f'总行数: {len(lines)}')
print(f'非空行数: {len(non_empty_lines)}')
print(f'段落数: {article.count("\\n\\n")}')

# 检查是否达到目标
print()
print('='*60)
if 1000 <= chinese_chars <= 1500:
    print(f'✅ 达到目标！中文字数 {chinese_chars} 在 1000-1500 范围内')
else:
    print(f'❌ 未达标！中文字数 {chinese_chars}，目标是 1000-1500')