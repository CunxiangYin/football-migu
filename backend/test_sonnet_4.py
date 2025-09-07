#!/usr/bin/env python
"""测试Sonnet 4.0 API"""

import os
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_sonnet_4():
    """测试Sonnet 4.0 (Claude 3.5 Sonnet V2)"""
    from app.core.claude_config import get_claude_client, CLAUDE_MODELS
    
    print("=" * 60)
    print("测试 Sonnet 4.0 API")
    print("=" * 60)
    
    # 显示所有可用模型
    print("\n可用模型:")
    for key, model_id in CLAUDE_MODELS.items():
        if "sonnet" in key.lower():
            print(f"  - {key}: {model_id}")
    
    # 获取客户端 (使用默认的Sonnet 4.0)
    client = get_claude_client()
    print(f"\n当前使用模型: {client.model}")
    print("这是最新的 Sonnet 4.0 (Claude 3.5 Sonnet V2, 2024年10月22日版本)")
    
    # 测试简单对话
    print("\n测试基础对话...")
    result = client.create_message(
        prompt="你好！请告诉我你是哪个版本的Claude模型？请用中文回答。",
        max_tokens=100
    )
    
    if result["success"]:
        print(f"✅ 响应成功!")
        print(f"模型回复: {result['content']}")
    else:
        print(f"❌ 请求失败: {result.get('error')}")
        return False
    
    # 测试预测生成
    print("\n\n测试足球预测生成...")
    test_data = {
        'home_team': {
            'name': '曼城',
            'league_position': 1,
            'recent_performance': '近5场4胜1平',
            'home_away_record': '主场10胜1平0负'
        },
        'away_team': {
            'name': '利物浦',
            'league_position': 2,
            'recent_performance': '近5场3胜1平1负',
            'home_away_record': '客场6胜2平2负'
        }
    }
    
    prediction_result = client.generate_prediction(test_data)
    
    if prediction_result["success"]:
        print(f"✅ 预测生成成功!")
        print(f"使用模型: {prediction_result['model']}")
        print(f"生成字符数: {len(prediction_result['prediction'])} 个字符")
        
        # 显示部分预测内容
        preview = prediction_result['prediction'][:300] + "..."
        print(f"\n预测内容预览:\n{preview}")
        
        # 显示token使用情况
        if prediction_result.get('usage'):
            usage = prediction_result['usage']
            print(f"\nToken使用情况:")
            print(f"  输入: {usage.get('input_tokens', 'N/A')}")
            print(f"  输出: {usage.get('output_tokens', 'N/A')}")
    else:
        print(f"❌ 预测生成失败: {prediction_result.get('error')}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Sonnet 4.0 API 测试完成!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_sonnet_4()
    if not success:
        sys.exit(1)