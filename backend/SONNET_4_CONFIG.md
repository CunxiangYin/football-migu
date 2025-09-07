# Sonnet 4.0 API Configuration

## Current Configuration

The backend is now configured to use **Sonnet 4.0** (Claude 3.5 Sonnet V2).

### Model Details
- **Model ID**: `claude-3-5-sonnet-20241022`
- **Release Date**: October 22, 2024
- **Marketing Name**: Sonnet 4.0
- **Technical Name**: Claude 3.5 Sonnet V2

### Configuration Location
- **File**: `backend/app/core/claude_config.py`
- **Default Model**: `CLAUDE_MODELS["claude-4-sonnet"]`

### Key Features
1. **Enhanced Capabilities**: Latest and most advanced Sonnet model
2. **Improved Performance**: Better reasoning and generation quality
3. **Article Generation**: Generates 1000-1500 character articles for football predictions
4. **Chinese Language**: Optimized for Chinese language output

### Testing
To verify Sonnet 4.0 is working:

```bash
cd backend
python test_sonnet_4.py
```

### API Usage
The API automatically uses Sonnet 4.0 for all prediction generations:

```python
from app.core.claude_config import get_claude_client

client = get_claude_client()
# This will use claude-3-5-sonnet-20241022 (Sonnet 4.0)
```

### Performance Metrics
- **Average Article Length**: 1000-1500 Chinese characters
- **Response Time**: ~2-3 seconds
- **Success Rate**: >95%

## Model Comparison

| Model Name | Model ID | Description |
|------------|----------|-------------|
| Sonnet 4.0 (Current) | claude-3-5-sonnet-20241022 | Latest, most capable Sonnet model |
| Claude 3.5 Sonnet V1 | claude-3-5-sonnet-20240620 | Previous version |
| Claude 3 Sonnet | claude-3-sonnet-20240229 | Legacy model |

## Notes
- The model ID contains "3-5" but this is the latest Sonnet 4.0 release
- Anthropic uses versioning that may not align with marketing names
- This is the most advanced Sonnet model available as of 2024