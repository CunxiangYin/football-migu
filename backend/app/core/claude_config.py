"""Claude API configuration and client management."""

import os
from typing import Optional, Dict, Any
import anthropic
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)

# Claude model versions
CLAUDE_MODELS = {
    # Claude 4 models (latest)
    "claude-4-opus": "claude-3-opus-20240229",  # Most capable model
    "claude-4-sonnet": "claude-3-5-sonnet-20241022",  # Claude 3.5 Sonnet (latest)
    "claude-4-haiku": "claude-3-haiku-20240307",  # Fast and cost-effective
    
    # Legacy models
    "claude-3-opus": "claude-3-opus-20240229",
    "claude-3-sonnet": "claude-3-sonnet-20240229",
    "claude-3-haiku": "claude-3-haiku-20240307",
}

# Default model to use
DEFAULT_MODEL = CLAUDE_MODELS["claude-4-sonnet"]  # Use Claude 3.5 Sonnet as default

class ClaudeClient:
    """Enhanced Claude API client with model management."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize Claude client.
        
        Args:
            api_key: Anthropic API key (defaults to env variable)
            model: Model to use (defaults to Claude 4 Sonnet)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model or DEFAULT_MODEL
        logger.info(f"Initialized Claude client with model: {self.model}")
    
    def create_message(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a message using Claude API.
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system: System prompt
            
        Returns:
            Response from Claude API
        """
        try:
            messages = [{"role": "user", "content": prompt}]
            
            # Add system message if provided
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }
            
            if system:
                kwargs["system"] = system
            
            logger.debug(f"Sending request to Claude API with model {self.model}")
            response = self.client.messages.create(**kwargs)
            
            return {
                "success": True,
                "content": response.content[0].text,
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens if hasattr(response, 'usage') else None,
                    "output_tokens": response.usage.output_tokens if hasattr(response, 'usage') else None
                }
            }
        except Exception as e:
            logger.error(f"Error calling Claude API: {e}")
            return {
                "success": False,
                "error": str(e),
                "model": self.model
            }
    
    def generate_prediction(
        self,
        match_data: Dict[str, Any],
        expert_style: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate match prediction using Claude 4.
        
        Args:
            match_data: Match information
            expert_style: Optional expert style to emulate
            
        Returns:
            Prediction result
        """
        system_prompt = """You are an expert football analyst with deep knowledge of statistics, 
        team dynamics, and betting markets. Provide detailed and insightful predictions based on data.
        Always respond in Chinese and maintain a professional tone."""
        
        if expert_style:
            system_prompt += f"\n\nAnalyze in the style of: {expert_style}"
        
        prompt = f"""基于以下数据，提供详细的比赛预测分析（1000-1500字）：

主队：{match_data.get('home_team', {}).get('name', '主队')}
- 联赛排名：第{match_data.get('home_team', {}).get('league_position', 'N/A')}位
- 近期战绩：{match_data.get('home_team', {}).get('recent_performance', 'N/A')}
- 主场战绩：{match_data.get('home_team', {}).get('home_away_record', 'N/A')}

客队：{match_data.get('away_team', {}).get('name', '客队')}
- 联赛排名：第{match_data.get('away_team', {}).get('league_position', 'N/A')}位
- 近期战绩：{match_data.get('away_team', {}).get('recent_performance', 'N/A')}
- 客场战绩：{match_data.get('away_team', {}).get('home_away_record', 'N/A')}

请提供：
1. 详细的基本面分析（300-400字）
2. 历史交锋分析（200-300字）
3. 伤停和阵容分析（200-300字）
4. 盘口和赔率解读（200-300字）
5. 综合预测和投注建议（200-300字）

要求：
- 使用专业术语
- 数据支撑观点
- 逻辑清晰
- 给出具体比分预测
- 提供置信度百分比"""

        result = self.create_message(
            prompt=prompt,
            system=system_prompt,
            max_tokens=4096,
            temperature=0.7
        )
        
        if result["success"]:
            return {
                "success": True,
                "prediction": result["content"],
                "model": result["model"],
                "usage": result.get("usage", {})
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "model": result["model"]
            }
    
    def set_model(self, model_key: str):
        """
        Change the model being used.
        
        Args:
            model_key: Key from CLAUDE_MODELS dict
        """
        if model_key in CLAUDE_MODELS:
            self.model = CLAUDE_MODELS[model_key]
            logger.info(f"Model changed to: {self.model}")
        else:
            raise ValueError(f"Invalid model key: {model_key}. Available: {list(CLAUDE_MODELS.keys())}")

# Global client instance (lazy initialization)
_claude_client: Optional[ClaudeClient] = None

def get_claude_client(model: Optional[str] = None) -> ClaudeClient:
    """
    Get or create Claude client instance.
    
    Args:
        model: Optional model override
        
    Returns:
        ClaudeClient instance
    """
    global _claude_client
    
    if _claude_client is None:
        _claude_client = ClaudeClient(model=model)
    elif model and _claude_client.model != model:
        _claude_client.model = model
    
    return _claude_client

def test_claude_api():
    """Test Claude API connection and model."""
    try:
        client = get_claude_client()
        result = client.create_message(
            prompt="Hello, please respond with 'API working' and the model version you are using.",
            max_tokens=50
        )
        
        if result["success"]:
            print(f"✅ Claude API test successful!")
            print(f"Model: {result['model']}")
            print(f"Response: {result['content']}")
            return True
        else:
            print(f"❌ Claude API test failed: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Error testing Claude API: {e}")
        return False

if __name__ == "__main__":
    # Test the API when running directly
    test_claude_api()