#!/usr/bin/env python
"""验证文章生成长度"""

import requests
import json

def test_api_article_length():
    """测试API返回的文章长度"""
    
    # Railway backend URL
    api_url = "https://web-production-ccc8.up.railway.app/api/v1/real-matches/generate-prediction/1001"
    
    print("=" * 60)
    print("测试API文章生成长度")
    print("=" * 60)
    
    try:
        # 发送POST请求
        response = requests.post(api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "success":
                content = data["data"]["content"]
                char_count = len(content)
                
                print(f"✅ API调用成功!")
                print(f"文章长度: {char_count} 个字符")
                
                # 检查是否符合要求
                if char_count >= 1000:
                    print(f"✅ 符合要求 (≥1000字符)")
                else:
                    print(f"❌ 不符合要求 (需要≥1000字符)")
                
                # 显示部分内容
                preview = content[:500] + "..." if len(content) > 500 else content
                print(f"\n文章预览:\n{preview}")
                
                # 显示专家信息
                expert = data["data"].get("expert", {})
                print(f"\n专家: {expert.get('name', 'N/A')}")
                print(f"胜率: {expert.get('win_rate', 'N/A')}%")
                
            else:
                print(f"❌ API返回错误: {data}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"响应: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    test_api_article_length()