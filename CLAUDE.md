# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Football match prediction and analysis system with real-time odds, expert predictions, and comprehensive match statistics. Full-stack application using Next.js frontend and FastAPI backend.

## Tech Stack

### Frontend
- **Next.js 14** - App router, server components
- **TypeScript** - Strict mode enabled
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Component library (Radix UI primitives)
- **React Query (TanStack Query v5)** - Data fetching and caching
- **Axios** - HTTP client

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy 2.0** - ORM with declarative models
- **SQLite** - Development database
- **Pydantic v2** - Data validation with BaseModel schemas
- **Uvicorn** - ASGI server

## Common Development Commands

### Quick Start
```bash
chmod +x start.sh && ./start.sh  # Starts both frontend and backend
```

### Frontend Commands
```bash
cd frontend
npm install              # Install dependencies
npm run dev             # Start development server (port 3000)
npm run build           # Build for production
npm run lint            # Run ESLint
npx tsc --noEmit       # TypeScript type checking
```

### Backend Commands
```bash
cd backend
python -m venv venv && source venv/bin/activate  # Setup virtual environment
pip install -r requirements.txt                   # Install dependencies
python main.py                                     # Start server (port 8000)
python start_server.py                             # Alternative start command
python seed_simple.py                              # Seed database with test data
pytest tests/                                      # Run tests
```

### Testing Commands
```bash
# Backend testing
cd backend && pytest tests/ -v

# Frontend type checking
cd frontend && npx tsc --noEmit
```

## Architecture

### Backend Structure
```
backend/
├── app/
│   ├── api/v1/          # API endpoints (FastAPI routers)
│   │   ├── endpoints/    # Individual endpoint modules
│   │   └── *.py         # Enhanced prediction endpoints
│   ├── domain/
│   │   ├── models/      # SQLAlchemy ORM models
│   │   └── schemas/     # Pydantic schemas (request/response)
│   ├── services/        # Business logic layer
│   ├── repositories/    # Data access layer
│   └── core/            # Config, database, logging
├── agents/              # AI prediction agents (Claude integration)
└── main.py             # Application entry point
```

### Frontend Structure
```
frontend/
├── app/                 # Next.js app directory
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   ├── predictions/    # Predictions list page
│   └── prediction/[id]/ # Prediction detail page
├── components/
│   ├── predictions/    # Prediction-specific components
│   └── ui/            # shadcn/ui components
├── hooks/             # Custom React hooks
├── lib/               # Utilities and API client
└── types/             # TypeScript type definitions
```

### API Architecture

The backend follows a layered architecture:
1. **Routers** (app/api/v1/) - Handle HTTP requests, validate input
2. **Services** (app/services/) - Business logic, orchestration
3. **Repositories** (app/repositories/) - Database operations
4. **Models** (app/domain/models/) - SQLAlchemy ORM entities
5. **Schemas** (app/domain/schemas/) - Pydantic models for validation

### Key API Endpoints
- `GET /api/v1/predictions` - List predictions with pagination
- `GET /api/v1/predictions/{id}` - Get prediction detail
- `GET /api/v1/real-matches` - List actual matches
- `GET /api/v1/experts` - List expert profiles
- `GET /api/v1/matches` - List matches with odds
- `GET /api/v1/statistics` - Get match statistics

### Frontend Data Flow
1. **API Client** (lib/api-client.ts) - Axios instance with interceptors
2. **Custom Hooks** (hooks/) - React Query hooks for data fetching
3. **Components** - Consume data via hooks, handle loading/error states
4. **Types** (types/) - Shared TypeScript interfaces

## Important Patterns

### Frontend Patterns
- Use `@/` path alias for imports (maps to frontend root)
- All API calls go through `lib/api-client.ts`
- Use React Query for server state management
- Components use shadcn/ui primitives with Tailwind styling
- Implement optimistic updates for user interactions

### Backend Patterns
- Use dependency injection via FastAPI's `Depends`
- Database sessions managed by `get_db` dependency
- Pydantic schemas for request/response validation
- Repository pattern for database operations
- Service layer for business logic

### Database Models
Key models include:
- **Match** - Football match with teams, scores, status
- **Prediction** - Expert predictions with analysis
- **Expert** - Expert profiles with credentials
- **Team** - Team information and statistics
- **BettingOdds** - Real-time betting odds

## Environment Configuration

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Backend (.env)
```
DATABASE_URL=sqlite:///./football_betting.db
ENVIRONMENT=development
DEBUG=true
```

## Development Workflow

1. **Start Services**: Run `./start.sh` to start both frontend and backend
2. **API Documentation**: Access Swagger UI at `http://localhost:8000/docs`
3. **Database**: SQLite database at `backend/football_betting.db`
4. **Hot Reload**: Both frontend and backend support hot reload in development
5. **Type Checking**: Run `npx tsc --noEmit` in frontend before committing

## Key Features

### Prediction System
- Expert predictions with detailed analysis
- Multiple prediction types (score, winner, goals)
- Confidence levels and reasoning
- Historical accuracy tracking

### Real-time Data
- Live match updates
- Dynamic odds updates
- Real-time statistics
- Match status tracking

### User Engagement
- Like/bookmark functionality
- Comment system
- Share predictions
- Follow experts

## Testing Approach

### Frontend Testing
- Type checking with TypeScript strict mode
- Component testing with React Testing Library
- API mocking with MSW (Mock Service Worker)

### Backend Testing
- Unit tests with pytest
- API endpoint testing with TestClient
- Mock data fixtures for consistent testing
- Database rollback after tests

## Deployment

### Frontend Deployment
- Vercel deployment via `vercel.json`
- Static export with `next build && next export`
- Environment variables in Vercel dashboard

### Backend Deployment
- Docker container with `Dockerfile.backend`
- Gunicorn for production WSGI server
- PostgreSQL for production database