# Football Betting Backend Service Design

## Architecture Overview

The Football Betting Backend Service is designed as a modular FastAPI application following clean architecture principles. The system provides comprehensive APIs for football match data, expert predictions, betting odds, and user engagement features.

### System Architecture
```
┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   FastAPI       │
│   Application   │     │   Backend       │
└─────────────────┘     └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │   SQLAlchemy    │
                        │      ORM        │
                        └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │   SQLite DB     │
                        │  (Development)   │
                        └─────────────────┘
```

## Service Components

### 1. API Layer (`/app/api`)
- **Routers**: Organize endpoints by domain (matches, experts, statistics)
- **Dependencies**: Shared dependencies for database sessions, authentication
- **Middleware**: CORS, logging, error handling

### 2. Domain Layer (`/app/domain`)
- **Models**: SQLAlchemy ORM models for database entities
- **Schemas**: Pydantic models for request/response validation
- **Enums**: Shared enumerations (match status, betting types)

### 3. Service Layer (`/app/services`)
- **Business Logic**: Core business rules and calculations
- **Data Processing**: Transform and aggregate data
- **External Services**: Integration points for future external APIs

### 4. Repository Layer (`/app/repositories`)
- **Database Operations**: CRUD operations for each entity
- **Query Optimization**: Complex queries and aggregations
- **Transaction Management**: Handle database transactions

### 5. Infrastructure Layer (`/app/core`)
- **Configuration**: Environment variables and settings
- **Database**: Connection management and migrations
- **Security**: Authentication and authorization utilities
- **Logging**: Structured logging configuration

## Data Models

### Expert Model
```python
Expert:
  - id: UUID
  - name: str
  - avatar_url: str
  - badges: List[Badge]
  - win_rate: float
  - avg_return: float
  - total_predictions: int
  - followers_count: int
  - recent_performance: List[Performance]
  - specializations: List[League]
```

### Match Model
```python
Match:
  - id: UUID
  - home_team: Team
  - away_team: Team
  - league: League
  - match_date: datetime
  - status: MatchStatus
  - venue: str
  - referee: str
  - weather_conditions: Weather
  - importance_level: int
```

### BettingOdds Model
```python
BettingOdds:
  - id: UUID
  - match_id: UUID
  - bookmaker: str
  - home_win: float
  - draw: float
  - away_win: float
  - over_2_5: float
  - under_2_5: float
  - btts_yes: float
  - btts_no: float
  - handicap_home: float
  - handicap_away: float
  - updated_at: datetime
```

### Prediction Model
```python
Prediction:
  - id: UUID
  - match_id: UUID
  - expert_id: UUID
  - prediction_type: PredictionType
  - predicted_outcome: str
  - confidence: float
  - stake_recommendation: StakeLevel
  - reasoning: str
  - created_at: datetime
```

### Analysis Model
```python
Analysis:
  - id: UUID
  - match_id: UUID
  - tactical_analysis: str
  - key_players: List[Player]
  - injury_report: List[Injury]
  - form_analysis: FormData
  - head_to_head: H2HData
  - statistical_edge: str
  - sentiment_score: float
```

### Statistics Model
```python
Statistics:
  - id: UUID
  - team_id: UUID
  - match_id: UUID
  - possession: float
  - shots: int
  - shots_on_target: int
  - corners: int
  - fouls: int
  - yellow_cards: int
  - red_cards: int
  - pass_accuracy: float
  - expected_goals: float
```

### Engagement Model
```python
Engagement:
  - id: UUID
  - match_id: UUID
  - views: int
  - likes: int
  - comments: int
  - shares: int
  - tips_received: int
  - last_activity: datetime
```

## API Endpoints

### Match Endpoints
- `GET /api/v1/matches` - List matches with filtering and pagination
- `GET /api/v1/matches/{match_id}` - Get detailed match information
- `GET /api/v1/matches/{match_id}/predictions` - Get all predictions for a match
- `GET /api/v1/matches/{match_id}/analysis` - Get match analysis
- `GET /api/v1/matches/{match_id}/statistics` - Get match statistics
- `GET /api/v1/matches/{match_id}/odds` - Get betting odds
- `POST /api/v1/matches/{match_id}/like` - Like a match prediction
- `POST /api/v1/matches/{match_id}/comment` - Add comment

### Expert Endpoints
- `GET /api/v1/experts` - List all experts
- `GET /api/v1/experts/{expert_id}` - Get expert details
- `GET /api/v1/experts/{expert_id}/predictions` - Get expert's predictions
- `GET /api/v1/experts/{expert_id}/statistics` - Get expert's performance stats
- `POST /api/v1/experts/{expert_id}/follow` - Follow/unfollow expert
- `GET /api/v1/experts/leaderboard` - Get expert rankings

### Statistics Endpoints
- `GET /api/v1/statistics/teams/{team_id}` - Get team statistics
- `GET /api/v1/statistics/leagues/{league_id}` - Get league statistics
- `GET /api/v1/statistics/trends` - Get betting trends

### User Engagement Endpoints
- `GET /api/v1/engagement/trending` - Get trending matches
- `GET /api/v1/engagement/popular-experts` - Get popular experts
- `POST /api/v1/engagement/tip` - Send tip to expert

## Database Schema

### Tables Structure
```sql
-- Experts table
CREATE TABLE experts (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    win_rate DECIMAL(5,2),
    avg_return DECIMAL(5,2),
    total_predictions INTEGER,
    followers_count INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Matches table
CREATE TABLE matches (
    id UUID PRIMARY KEY,
    home_team_id UUID,
    away_team_id UUID,
    league_id UUID,
    match_date TIMESTAMP,
    status VARCHAR(50),
    venue VARCHAR(200),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Predictions table
CREATE TABLE predictions (
    id UUID PRIMARY KEY,
    match_id UUID REFERENCES matches(id),
    expert_id UUID REFERENCES experts(id),
    prediction_type VARCHAR(50),
    predicted_outcome VARCHAR(100),
    confidence DECIMAL(5,2),
    stake_level VARCHAR(20),
    reasoning TEXT,
    created_at TIMESTAMP
);

-- Additional tables for odds, analysis, statistics, etc.
```

## Security Considerations

### Authentication & Authorization
- JWT token-based authentication for future user features
- API key authentication for external service integration
- Rate limiting per IP/user
- Input validation on all endpoints

### Data Protection
- SQL injection prevention through parameterized queries
- XSS protection through proper data sanitization
- CORS configuration for allowed origins
- Environment-based configuration management

## Performance Optimization

### Caching Strategy
- Redis integration for frequently accessed data
- Response caching for static content
- Database query result caching

### Database Optimization
- Indexed columns for frequent queries
- Eager loading for related data
- Query optimization for complex aggregations
- Connection pooling

### API Optimization
- Pagination for list endpoints
- Field filtering for partial responses
- Async operations for I/O bound tasks
- Background tasks for heavy computations

## Monitoring & Logging

### Logging Strategy
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Request/response logging middleware
- Error tracking and alerting

### Metrics
- API response times
- Database query performance
- Error rates by endpoint
- User engagement metrics

## Deployment Considerations

### Development Environment
- SQLite database for rapid development
- Mock data generation scripts
- Hot reload with uvicorn
- Debug mode with detailed error messages

### Production Environment
- PostgreSQL database for production
- Environment variable configuration
- Docker containerization
- Health check endpoints
- Graceful shutdown handling

### Scaling Strategy
- Horizontal scaling with load balancer
- Database read replicas
- Caching layer with Redis
- Async task queue for background jobs
- CDN for static assets

## Testing Strategy

### Unit Tests
- Test individual functions and methods
- Mock external dependencies
- Test data validation
- Test business logic

### Integration Tests
- Test API endpoints
- Test database operations
- Test service integrations
- Test error handling

### Performance Tests
- Load testing with multiple concurrent users
- Stress testing for system limits
- Database query performance testing
- API response time benchmarks

## Future Enhancements

### Phase 2 Features
- Real-time match updates via WebSocket
- Push notifications for predictions
- Machine learning for prediction accuracy
- Social features (comments, discussions)
- Payment integration for premium features

### Phase 3 Features
- Mobile API optimization
- GraphQL API option
- Multi-language support
- Advanced analytics dashboard
- Third-party data provider integration

## API Response Standards

### Success Response
```json
{
  "status": "success",
  "data": {...},
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
  }
}
```

### Error Response
```json
{
  "status": "error",
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Match not found",
    "details": {...}
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "uuid"
  }
}
```

### Pagination Response
```json
{
  "status": "success",
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  },
  "metadata": {...}
}
```