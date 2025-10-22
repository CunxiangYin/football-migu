# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only the simple server
COPY server.py ./

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start the simple server
CMD ["python", "server.py"]