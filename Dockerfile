# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/ ./backend/

# Copy startup scripts
COPY railway_start.py ./

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Create data directory for SQLite
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app/backend
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV DATABASE_URL=sqlite:///app/data/football_betting.db

# Start the application directly
CMD ["python", "railway_start.py"]