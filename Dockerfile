# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/ ./backend/

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Create data directory for SQLite
RUN mkdir -p /app/data

# Expose port (Railway will override this)
EXPOSE 8000

# Start the application
CMD ["python", "backend/start_server.py"]