# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/ ./backend/
COPY requirements.txt ./backend/

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