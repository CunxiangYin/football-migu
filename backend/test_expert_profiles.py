#!/usr/bin/env python3
"""
Test script to demonstrate the expert prediction profiles functionality
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from agents.prediction_experts import prediction_experts, ExpertiseArea, WritingStyle

def test_expert_profiles():
    """Test the expert profiles system"""
    
    print("=== Football Prediction Expert Profiles Test ===\n")
    
    # Get all experts
    experts = prediction_experts.get_all_experts()
    print(f"Total experts loaded: {len(experts)}\n")
    
    # Display all expert summaries
    print("Expert Roster:")
    print("-" * 60)
    for expert in experts:
        print(f"🎯 {expert.name} ({expert.nickname})")
        print(f"   Expertise: {expert.primary_expertise.value}")
        print(f"   Style: {expert.writing_style.value}")
        print(f"   Win Rate: {expert.win_rate}%")
        print(f"   Followers: {expert.followers_count:,}")
        print(f"   Bio: {expert.bio[:80]}...")
        print()
    
    # Test specific expert retrieval
    print("\n" + "="*60)
    print("Testing Expert Retrieval:")
    print("-" * 60)
    
    # Get data wizard
    data_expert = prediction_experts.get_expert_by_nickname("The Data Wizard")
    if data_expert:
        print(f"Found: {data_expert.name}")
        print(f"Specializations: {', '.join(data_expert.specializations)}")
        print(f"Key Metrics: {', '.join(data_expert.key_metrics)}")
        print(f"Signature Phrases: {data_expert.signature_phrases[:2]}")
    
    print()
    
    # Get experts by expertise area
    stats_experts = prediction_experts.get_experts_by_expertise(ExpertiseArea.STATISTICS)
    print(f"Statistical Analysis Experts: {len(stats_experts)}")
    for expert in stats_experts:
        print(f"  - {expert.nickname}")
    
    # Test article generation
    print("\n" + "="*60)
    print("Testing Article Generation:")
    print("-" * 60)
    
    # Sample match data
    match_info = {
        "home_team": "Manchester United",
        "away_team": "Liverpool",
        "league": "Premier League",
        "match_time": "2024-09-15 16:30",
        "venue": "Old Trafford"
    }
    
    odds_info = {
        "home_win": 2.50,
        "draw": 3.40,
        "away_win": 2.80,
        "asian_handicap": "主队+0.25",
        "over_under": "2.5/3球"
    }
    
    historical_data = {
        "h2h_record": "近5次交锋: 2胜1平2负",
        "home_record": "主场3胜1平1负",
        "away_record": "客场1胜2平2负"
    }
    
    # Generate articles from different expert perspectives
    expert_keys = ["data_wizard", "tactician", "handicap_master"]
    
    for expert_key in expert_keys:
        if expert_key in prediction_experts.experts:
            print(f"\n📝 {prediction_experts.experts[expert_key].nickname} Analysis:")
            print("-" * 40)
            
            try:
                article = prediction_experts.generate_expert_article(
                    expert_key=expert_key,
                    match_info=match_info,
                    odds_info=odds_info,
                    historical_data=historical_data
                )
                
                print(f"Title: {article['title']}")
                print(f"Opening: {article['opening'][:100]}...")
                print(f"Prediction: {article['prediction']}")
                print(f"Confidence: {article['confidence']}%")
                print(f"Betting Advice: {article['betting_advice']['primary_bet']} ({article['betting_advice']['stake']})")
                
            except Exception as e:
                print(f"Error generating article: {e}")
    
    print("\n" + "="*60)
    print("Expert Profile Features:")
    print("-" * 60)
    
    # Show different writing styles
    styles = set(expert.writing_style for expert in experts)
    print(f"Writing Styles Available: {len(styles)}")
    for style in sorted(styles, key=lambda x: x.value):
        style_experts = [e.nickname for e in experts if e.writing_style == style]
        print(f"  {style.value}: {', '.join(style_experts)}")
    
    print()
    
    # Show expertise areas
    areas = set(expert.primary_expertise for expert in experts)
    print(f"Expertise Areas Covered: {len(areas)}")
    for area in sorted(areas, key=lambda x: x.value):
        area_experts = [e.nickname for e in experts if e.primary_expertise == area]
        print(f"  {area.value}: {', '.join(area_experts)}")
    
    print("\n" + "="*60)
    print("Test completed successfully! 🎉")
    print("The expert prediction system is ready for integration.")


def show_expert_specialties():
    """Show detailed specialties of each expert"""
    print("\n" + "="*60)
    print("EXPERT SPECIALIZATION DETAILS:")
    print("="*60)
    
    experts = prediction_experts.get_all_experts()
    
    for expert in experts:
        print(f"\n🔥 {expert.nickname} - {expert.name}")
        print(f"Primary Focus: {expert.primary_expertise.value}")
        print(f"Writing Style: {expert.writing_style.value}")
        print(f"Tone Keywords: {', '.join(expert.tone_keywords[:3])}...")
        print(f"Analysis Priorities:")
        for priority in expert.analysis_priorities:
            print(f"  • {priority}")
        print(f"Preferred Bets: {', '.join(expert.preferred_bet_types)}")
        print(f"Performance: {expert.win_rate}% win rate, {expert.avg_return:.2f} avg return")
        print("-" * 50)


if __name__ == "__main__":
    test_expert_profiles()
    show_expert_specialties()