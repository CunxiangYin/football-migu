# Use Python 3.11 slim image - Updated to force rebuild
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY backend/requirements.txt ./backend/requirements.txt

# Copy backend files
COPY backend/ ./backend/

# Install dependencies
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for SQLite
RUN mkdir -p /app/backend/data

# Set environment variables
ENV PYTHONPATH=/app/backend
ENV HOST=0.0.0.0

# Expose port (Railway will set PORT dynamically)
EXPOSE ${PORT:-8000}

# Start the application from the backend directory
CMD ["python", "start_server.py"]