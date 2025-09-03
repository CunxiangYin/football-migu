#!/bin/bash

# Deployment script for production server
# Usage: ./deploy.sh [docker|pm2|systemd]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Football Betting System - Production Deployment${NC}"
echo "================================================"

# Check deployment method
METHOD=${1:-docker}

# Function to check requirements
check_requirements() {
    local missing=()
    
    if [ "$METHOD" = "docker" ]; then
        command -v docker >/dev/null 2>&1 || missing+=("docker")
        command -v docker-compose >/dev/null 2>&1 || missing+=("docker-compose")
    elif [ "$METHOD" = "pm2" ]; then
        command -v node >/dev/null 2>&1 || missing+=("node")
        command -v npm >/dev/null 2>&1 || missing+=("npm")
        command -v pm2 >/dev/null 2>&1 || missing+=("pm2")
        command -v python3 >/dev/null 2>&1 || missing+=("python3")
    elif [ "$METHOD" = "systemd" ]; then
        command -v node >/dev/null 2>&1 || missing+=("node")
        command -v npm >/dev/null 2>&1 || missing+=("npm")
        command -v python3 >/dev/null 2>&1 || missing+=("python3")
        command -v systemctl >/dev/null 2>&1 || missing+=("systemctl")
    fi
    
    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}Error: Missing required tools: ${missing[*]}${NC}"
        exit 1
    fi
}

# Docker deployment
deploy_docker() {
    echo -e "${YELLOW}📦 Deploying with Docker...${NC}"
    
    # Build images
    echo "Building Docker images..."
    docker-compose build
    
    # Start services
    echo "Starting services..."
    docker-compose up -d
    
    # Wait for services to be ready
    echo "Waiting for services to be ready..."
    sleep 10
    
    # Check health
    if curl -f http://localhost/health >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Services are healthy${NC}"
    else
        echo -e "${YELLOW}⚠️  Services may still be starting...${NC}"
    fi
    
    echo -e "${GREEN}✅ Docker deployment complete${NC}"
    echo "Services:"
    echo "  - Frontend: http://localhost (port 80)"
    echo "  - Backend API: http://localhost/api"
    echo "  - API Docs: http://localhost/docs"
}

# PM2 deployment
deploy_pm2() {
    echo -e "${YELLOW}📦 Deploying with PM2...${NC}"
    
    # Backend setup
    echo "Setting up backend..."
    cd backend
    
    # Create virtual environment
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -r requirements.txt
    
    # Start backend with PM2
    pm2 start start_server.py --name football-backend --interpreter python3
    
    cd ..
    
    # Frontend setup
    echo "Setting up frontend..."
    cd frontend
    
    # Install dependencies
    npm install
    npm run build
    
    # Start frontend with PM2
    pm2 start npm --name football-frontend -- start
    
    cd ..
    
    # Save PM2 configuration
    pm2 save
    pm2 startup
    
    echo -e "${GREEN}✅ PM2 deployment complete${NC}"
    echo "Services managed by PM2:"
    pm2 list
}

# Systemd deployment
deploy_systemd() {
    echo -e "${YELLOW}📦 Deploying with systemd...${NC}"
    
    # Create systemd service for backend
    sudo tee /etc/systemd/system/football-backend.service > /dev/null <<EOF
[Unit]
Description=Football Betting Backend API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)/backend
Environment="PATH=$(pwd)/backend/venv/bin"
ExecStart=$(pwd)/backend/venv/bin/python $(pwd)/backend/start_server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
    
    # Create systemd service for frontend
    sudo tee /etc/systemd/system/football-frontend.service > /dev/null <<EOF
[Unit]
Description=Football Betting Frontend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)/frontend
ExecStart=/usr/bin/npm start
Restart=on-failure
Environment="NODE_ENV=production"

[Install]
WantedBy=multi-user.target
EOF
    
    # Setup services
    echo "Setting up backend..."
    cd backend
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    echo "Setting up frontend..."
    cd frontend
    npm install
    npm run build
    cd ..
    
    # Enable and start services
    sudo systemctl daemon-reload
    sudo systemctl enable football-backend
    sudo systemctl enable football-frontend
    sudo systemctl start football-backend
    sudo systemctl start football-frontend
    
    echo -e "${GREEN}✅ Systemd deployment complete${NC}"
    echo "Check service status:"
    echo "  sudo systemctl status football-backend"
    echo "  sudo systemctl status football-frontend"
}

# Nginx setup (optional)
setup_nginx() {
    echo -e "${YELLOW}🔧 Setting up Nginx...${NC}"
    
    # Check if nginx is installed
    if ! command -v nginx >/dev/null 2>&1; then
        echo "Installing Nginx..."
        sudo apt-get update
        sudo apt-get install -y nginx
    fi
    
    # Copy nginx configuration
    sudo cp nginx.conf /etc/nginx/sites-available/football-betting
    sudo ln -sf /etc/nginx/sites-available/football-betting /etc/nginx/sites-enabled/
    
    # Test configuration
    sudo nginx -t
    
    # Restart nginx
    sudo systemctl restart nginx
    
    echo -e "${GREEN}✅ Nginx configured${NC}"
}

# Main deployment flow
check_requirements

case $METHOD in
    docker)
        deploy_docker
        ;;
    pm2)
        deploy_pm2
        echo -e "${YELLOW}Do you want to setup Nginx? (y/n)${NC}"
        read -r response
        if [[ "$response" == "y" ]]; then
            setup_nginx
        fi
        ;;
    systemd)
        deploy_systemd
        echo -e "${YELLOW}Do you want to setup Nginx? (y/n)${NC}"
        read -r response
        if [[ "$response" == "y" ]]; then
            setup_nginx
        fi
        ;;
    *)
        echo -e "${RED}Invalid deployment method. Use: docker, pm2, or systemd${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "================================================"
echo "Access your application:"
echo "  - Frontend: http://your-server-ip"
echo "  - Backend API: http://your-server-ip:8000"
echo "  - API Docs: http://your-server-ip:8000/docs"
echo ""
echo "⚠️  Remember to:"
echo "  1. Update domain names in configuration files"
echo "  2. Configure firewall rules (ports 80, 443, 8000, 3000)"
echo "  3. Set up SSL certificates for HTTPS"
echo "  4. Update environment variables for production"