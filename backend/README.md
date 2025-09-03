# Football Betting Backend API

A comprehensive FastAPI backend service for football match betting predictions and analysis.

## Features

- **Match Management**: Browse matches with detailed information
- **Expert Predictions**: View predictions from betting experts
- **Betting Odds**: Compare odds from multiple bookmakers
- **Match Analysis**: Tactical analysis, team form, and head-to-head statistics
- **Statistics**: Comprehensive match and team statistics
- **Engagement Tracking**: Likes, comments, shares, and trending scores
- **RESTful API**: Clean, well-documented API endpoints
- **Mock Data**: Comprehensive mock data for development

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLAlchemy ORM with SQLite (development) / PostgreSQL (production)
- **Validation**: Pydantic
- **Authentication**: JWT (prepared for implementation)
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## Project Structure

```
backend/
├── app/
│   ├── api/            # API endpoints
│   ├── core/           # Core configuration
│   ├── domain/         # Models and schemas
│   ├── services/       # Business logic
│   └── utils/          # Utilities
├── tests/              # Test files
├── main.py             # Application entry point
├── run.py              # Run script
└── requirements.txt    # Dependencies
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment variables:
```bash
cp .env.example .env
```

4. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

## API Endpoints

### Matches
- `GET /api/v1/matches` - List all matches with filtering
- `GET /api/v1/matches/{match_id}` - Get match details
- `GET /api/v1/matches/{match_id}/analysis` - Get match analysis
- `GET /api/v1/matches/{match_id}/statistics` - Get match statistics
- `GET /api/v1/matches/{match_id}/predictions` - Get match predictions
- `GET /api/v1/matches/{match_id}/odds` - Get betting odds
- `POST /api/v1/matches/{match_id}/like` - Like a match

### Experts
- `GET /api/v1/experts` - List all experts
- `GET /api/v1/experts/{expert_id}` - Get expert details
- `GET /api/v1/experts/{expert_id}/predictions` - Get expert predictions
- `GET /api/v1/experts/{expert_id}/statistics` - Get expert statistics
- `GET /api/v1/experts/leaderboard` - Get expert rankings
- `POST /api/v1/experts/{expert_id}/follow` - Follow/unfollow expert

### Statistics
- `GET /api/v1/statistics/teams/{team_id}` - Get team statistics
- `GET /api/v1/statistics/leagues/{league_id}` - Get league statistics
- `GET /api/v1/statistics/trends` - Get betting trends
- `GET /api/v1/statistics/comparison` - Compare two teams

## Development

### Mock Data
The application automatically seeds mock data in development mode on first run. This includes:
- 20 teams
- 10 experts
- 30 matches
- Predictions, odds, analysis, and statistics

### Database
- Development: SQLite database (`football_betting.db`)
- Production: Configure PostgreSQL in `.env`

### Testing
```bash
pytest tests/
```

## Environment Variables

Key environment variables (see `.env.example`):
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key
- `CORS_ORIGINS`: Allowed CORS origins
- `LOG_LEVEL`: Logging level

## Error Handling

The API uses consistent error responses:
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": {}
  }
}
```

## Pagination

List endpoints support pagination:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

Response includes pagination metadata:
```json
{
  "status": "success",
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## Future Enhancements

- [ ] User authentication and authorization
- [ ] WebSocket support for live updates
- [ ] Redis caching layer
- [ ] External data provider integration
- [ ] Machine learning predictions
- [ ] Payment integration
- [ ] Email notifications
- [ ] Rate limiting

## License

MIT