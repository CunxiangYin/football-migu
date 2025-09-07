#!/usr/bin/env python
"""测试Claude 4.0 API集成"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Set environment variables - load from .env file
from dotenv import load_dotenv
load_dotenv()

# Ensure API key is set
if not os.getenv('ANTHROPIC_API_KEY'):
    print("❌ Please set ANTHROPIC_API_KEY in .env file")
    sys.exit(1)

def test_claude_4_prediction():
    """测试使用Claude 4.0生成预测"""
    from app.core.claude_config import get_claude_client
    
    print("=" * 60)
    print("测试Claude 4.0 (3.5 Sonnet) 预测生成")
    print("=" * 60)
    
    # 获取客户端
    client = get_claude_client()
    print(f"✅ 使用模型: {client.model}")
    
    # 测试数据
    match_data = {
        'home_team': {
            'name': '曼联',
            'league_position': 3,
            'recent_performance': '近5场3胜1平1负',
            'home_away_record': '主场8胜2平1负'
        },
        'away_team': {
            'name': '切尔西',
            'league_position': 5,
            'recent_performance': '近5场2胜2平1负',
            'home_away_record': '客场4胜3平3负'
        }
    }
    
    # 生成预测
    result = client.generate_prediction(match_data)
    
    if result["success"]:
        print(f"\n✅ 预测生成成功!")
        print(f"模型: {result['model']}")
        print(f"字符数: {len(result['prediction'])} 个字符")
        
        # 显示部分内容
        preview = result['prediction'][:500] + "..." if len(result['prediction']) > 500 else result['prediction']
        print(f"\n预测内容预览:\n{preview}")
        
        # 显示token使用情况
        if result.get('usage'):
            print(f"\nToken使用:")
            print(f"- 输入: {result['usage'].get('input_tokens', 'N/A')}")
            print(f"- 输出: {result['usage'].get('output_tokens', 'N/A')}")
    else:
        print(f"❌ 预测生成失败: {result.get('error')}")
    
    return result

def test_enhanced_writer():
    """测试增强版写作器"""
    from agents.enhanced_football_writer import (
        EnhancedFootballWriter, MatchInfo, TeamInfo, OddsInfo, HistoricalData
    )
    
    print("\n" + "=" * 60)
    print("测试增强版写作器 (1000-1500字)")
    print("=" * 60)
    
    writer = EnhancedFootballWriter()
    
    # 创建测试数据
    home_team = TeamInfo(
        name="曼联",
        recent_form=['W', 'W', 'D', 'L', 'W'],
        league_position=3,
        home_away_record="主场8胜2平1负",
        key_players_status={"布鲁诺": "健康", "拉什福德": "健康"},
        recent_performance="近5场3胜1平1负，进11球失5球"
    )
    
    away_team = TeamInfo(
        name="切尔西",
        recent_form=['L', 'D', 'W', 'D', 'W'],
        league_position=5,
        home_away_record="客场4胜3平3负",
        key_players_status={"恩佐": "健康", "斯特林": "轻伤"},
        recent_performance="近5场2胜2平1负，进8球失7球"
    )
    
    match_info = MatchInfo(
        home_team=home_team,
        away_team=away_team,
        league="英超",
        match_time="2024-01-15 20:00",
        venue="老特拉福德球场",
        importance="关键战役",
        weather="晴朗"
    )
    
    odds_info = OddsInfo(
        home_win=2.10,
        draw=3.30,
        away_win=3.40,
        asian_handicap="主队-0.5",
        over_under="2.5"
    )
    
    historical_data = HistoricalData(
        h2h_results=[
            {"date": "2023-10-15", "score": "2-1", "winner": "home"},
            {"date": "2023-04-20", "score": "1-1", "winner": "draw"},
            {"date": "2022-11-25", "score": "1-2", "winner": "away"}
        ],
        home_team_home_record="主场对切尔西3胜1平1负",
        away_team_away_record="客场对曼联1胜1平3负"
    )
    
    # 生成文章
    result = writer.generate_prediction(match_info, odds_info, historical_data)
    
    # 提取文章内容
    if isinstance(result, dict):
        article = result.get('content', '')
    else:
        article = result
    
    # 统计字符数
    char_count = len(article)
    
    print(f"\n✅ 文章生成成功!")
    print(f"字符数: {char_count} 个字符")
    print(f"是否符合要求: {'✅ 是' if 1000 <= char_count <= 1500 else '❌ 否'}")
    
    # 显示文章结构
    if article:
        sections = article.split('\n\n')
        print(f"\n文章结构 ({len(sections)} 个段落):")
        for i, section in enumerate(sections[:3], 1):
            print(f"  段落 {i}: {len(section)} 个字符")
    
    return article

if __name__ == "__main__":
    # 测试Claude 4.0
    claude_result = test_claude_4_prediction()
    
    # 测试增强版写作器
    article = test_enhanced_writer()
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成!")
    print("=" * 60)