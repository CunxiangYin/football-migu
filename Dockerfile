# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/ ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for SQLite
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8000
ENV DATABASE_URL=sqlite:///app/data/football_betting.db
ENV ENVIRONMENT=production
ENV DEBUG=false

# Expose port
EXPOSE 8000

# Start the application directly
CMD ["python", "main.py"]