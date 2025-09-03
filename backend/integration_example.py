#!/usr/bin/env python3
"""
Integration example showing how to use expert prediction profiles
with the existing football prediction system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from agents.prediction_experts import prediction_experts, ExpertiseArea
from agents.football_prediction_writer import FootballPredictionWriter, MatchInfo, TeamInfo, OddsInfo, HistoricalData

def demonstrate_expert_integration():
    """Demonstrate how to integrate expert profiles with existing system"""
    
    print("=== Expert Prediction System Integration Demo ===\n")
    
    # Create sample match data using existing data structures
    home_team = TeamInfo(
        name="Manchester United",
        recent_form=["W", "W", "D", "L", "W"],
        league_position=3,
        home_away_record="主场8胜3平2负",
        key_players_status={"Marcus Rashford": "健康", "Bruno Fernandes": "健康"},
        recent_performance="近5场4胜1负，状态出色，攻击力强劲"
    )
    
    away_team = TeamInfo(
        name="Liverpool",
        recent_form=["L", "W", "W", "D", "L"],
        league_position=6,
        home_away_record="客场5胜4平4负",
        key_players_status={"Mohamed Salah": "健康", "Virgil van Dijk": "轻伤"},
        recent_performance="近5场3胜1平1负，客场表现一般，防守端有漏洞"
    )
    
    match_info = MatchInfo(
        home_team=home_team,
        away_team=away_team,
        league="Premier League",
        match_time="2024-09-15 16:30",
        venue="Old Trafford",
        weather="晴天，18°C，微风"
    )
    
    odds_info = OddsInfo(
        home_win=2.20,
        draw=3.50,
        away_win=2.90,
        asian_handicap="主队-0.25",
        over_under="2.5/3球"
    )
    
    historical_data = HistoricalData(
        h2h_results=[
            {"date": "2024-04-07", "score": "2-2", "winner": "draw"},
            {"date": "2023-12-17", "score": "1-0", "winner": "home"},
            {"date": "2023-08-19", "score": "1-3", "winner": "away"},
            {"date": "2023-03-05", "score": "2-1", "winner": "home"},
            {"date": "2022-10-23", "score": "1-1", "winner": "draw"}
        ],
        home_team_home_record="主场对利物浦近5场3胜1平1负",
        away_team_away_record="客场对曼联近5场1胜1平3负"
    )
    
    # Convert to dictionary format for expert system
    match_data = {
        "home_team": match_info.home_team.name,
        "away_team": match_info.away_team.name,
        "league": match_info.league,
        "venue": match_info.venue,
        "weather": match_info.weather
    }
    
    odds_data = {
        "home_win": odds_info.home_win,
        "draw": odds_info.draw,
        "away_win": odds_info.away_win,
        "asian_handicap": odds_info.asian_handicap,
        "over_under": odds_info.over_under
    }
    
    historical_dict = {
        "h2h_results": historical_data.h2h_results,
        "home_record": historical_data.home_team_home_record,
        "away_record": historical_data.away_team_away_record
    }
    
    # Generate predictions from different expert perspectives
    expert_keys = ["data_wizard", "tactician", "handicap_master", "goal_prophet", "value_hunter"]
    
    print("🎯 Multi-Expert Analysis Results:\n")
    print("="*80)
    
    for expert_key in expert_keys:
        expert_profile = prediction_experts.experts[expert_key]
        
        print(f"\n📊 {expert_profile.nickname} ({expert_profile.name})")
        print(f"Expertise: {expert_profile.primary_expertise.value}")
        print(f"Writing Style: {expert_profile.writing_style.value}")
        print("-" * 60)
        
        # Generate expert analysis
        article = prediction_experts.generate_expert_article(
            expert_key=expert_key,
            match_info=match_data,
            odds_info=odds_data,
            historical_data=historical_dict
        )
        
        # Display key insights
        print(f"Title: {article['title']}")
        print(f"Confidence: {article['confidence']}%")
        print(f"Prediction: {article['prediction']}")
        
        betting_advice = article['betting_advice']
        print(f"Betting Advice: {betting_advice['primary_bet']} ({betting_advice['stake']})")
        print(f"Reasoning: {betting_advice['reasoning']}")
        
        # Show one section as example
        if '专业分析' in article['sections']:
            analysis = article['sections']['专业分析']
            print(f"\nSpecialty Analysis Preview:")
            print(f"{analysis[:200]}..." if len(analysis) > 200 else analysis)
        
        print("=" * 60)
    
    # Compare expert recommendations
    print(f"\n📈 Expert Consensus Analysis:")
    print("-" * 40)
    
    recommendations = {}
    confidences = []
    
    for expert_key in expert_keys:
        article = prediction_experts.generate_expert_article(
            expert_key=expert_key,
            match_info=match_data,
            odds_info=odds_data,
            historical_data=historical_dict
        )
        
        expert = prediction_experts.experts[expert_key]
        betting_advice = article['betting_advice']
        primary_bet = betting_advice['primary_bet']
        
        if primary_bet not in recommendations:
            recommendations[primary_bet] = []
        recommendations[primary_bet].append(expert.nickname)
        confidences.append(article['confidence'])
    
    print(f"Average Expert Confidence: {sum(confidences)/len(confidences):.1f}%")
    print(f"\nBetting Recommendations:")
    for bet_type, experts in recommendations.items():
        print(f"  {bet_type}: {', '.join(experts)}")
    
    # Show how to use with original FootballPredictionWriter
    print(f"\n🔄 Integration with Original Writer:")
    print("-" * 40)
    
    original_writer = FootballPredictionWriter()
    original_prediction = original_writer.generate_prediction(
        match_info=match_info,
        odds_info=odds_info,
        historical_data=historical_data,
        expert_confidence=85
    )
    
    print(f"Original System Prediction: {original_prediction['predicted_score']}")
    print(f"Original Confidence: {original_prediction['confidence']}%")
    print(f"Original Recommendation: {original_prediction['recommendation']['selection']}")
    
    print(f"\n✅ Integration Complete!")
    print(f"The expert system can work alongside or replace the original prediction writer.")
    print(f"Multiple expert perspectives provide richer analysis and better user engagement.")


def show_expert_specialization_matrix():
    """Show which experts are best for different types of matches"""
    
    print(f"\n📋 Expert Specialization Matrix:")
    print("="*60)
    
    match_types = {
        "Derby Matches": ["mind_reader", "historian", "home_analyst"],
        "High-Scoring Games": ["goal_prophet", "data_wizard", "tactician"],
        "Tight Defensive Games": ["tactician", "handicap_master", "value_hunter"],
        "Weather-Affected Games": ["weather_watcher", "home_analyst", "tactician"],
        "Injury-Hit Teams": ["medic", "data_wizard", "value_hunter"],
        "Asian Market Focus": ["handicap_master", "value_hunter", "data_wizard"],
        "Historical Rivalries": ["historian", "mind_reader", "home_analyst"],
        "Value Betting Opportunities": ["value_hunter", "handicap_master", "data_wizard"]
    }
    
    for match_type, recommended_experts in match_types.items():
        print(f"\n🎮 {match_type}:")
        for expert_key in recommended_experts:
            if expert_key in prediction_experts.experts:
                expert = prediction_experts.experts[expert_key]
                print(f"   • {expert.nickname} - {expert.primary_expertise.value}")


if __name__ == "__main__":
    demonstrate_expert_integration()
    show_expert_specialization_matrix()