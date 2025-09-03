#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Football Betting Application${NC}"
echo "=================================="

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Start Backend
echo -e "\n${YELLOW}📦 Starting Backend Service...${NC}"
cd backend

# Check if backend port is already in use
if check_port 8000; then
    echo -e "${RED}❌ Port 8000 is already in use. Please stop the existing service.${NC}"
    exit 1
fi

# Install backend dependencies
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Start backend in background
echo "Starting FastAPI server..."
python start_server.py &
BACKEND_PID=$!
echo -e "${GREEN}✅ Backend started (PID: $BACKEND_PID)${NC}"

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
sleep 5

# Start Frontend
echo -e "\n${YELLOW}📱 Starting Frontend Service...${NC}"
cd ../frontend

# Check if frontend port is already in use
if check_port 3000; then
    echo -e "${RED}❌ Port 3000 is already in use. Please stop the existing service.${NC}"
    kill $BACKEND_PID
    exit 1
fi

# Install frontend dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start frontend
echo "Starting Next.js server..."
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✅ Frontend started (PID: $FRONTEND_PID)${NC}"

echo -e "\n${GREEN}🎉 Application is running!${NC}"
echo "=================================="
echo -e "Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "Backend API: ${GREEN}http://localhost:8000${NC}"
echo -e "API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo "=================================="
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}\n"

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Stopping services...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Services stopped.${NC}"
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup INT

# Wait for processes
wait $BACKEND_PID $FRONTEND_PID