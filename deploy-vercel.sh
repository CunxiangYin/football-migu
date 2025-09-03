#!/bin/bash

# Vercel + Railway Deployment Script
# This script helps deploy the frontend to Vercel and backend to Railway

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 Football Prediction System - Vercel Deployment${NC}"
echo "=================================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}Vercel CLI not found. Installing...${NC}"
    npm i -g vercel
fi

echo ""
echo -e "${GREEN}📋 Deployment Steps:${NC}"
echo ""
echo -e "${YELLOW}Step 1: Deploy Backend to Railway${NC}"
echo "----------------------------------------"
echo "1. Visit: https://railway.app/new/github"
echo "2. Select repository: CunxiangYin/football-migu"
echo "3. Railway will auto-detect Python app"
echo "4. Wait for deployment to complete"
echo "5. Copy the deployment URL"
echo ""
read -p "Enter your Railway backend URL (e.g., https://xxx.railway.app): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo -e "${RED}Error: Backend URL is required${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Deploy Frontend to Vercel${NC}"
echo "----------------------------------------"

# Update frontend environment
cd frontend

# Create .env.production.local with the backend URL
cat > .env.production.local << EOF
NEXT_PUBLIC_API_URL=${BACKEND_URL}/api/v1
NEXT_PUBLIC_APP_URL=https://football-migu.vercel.app
EOF

echo -e "${GREEN}✓ Environment configured${NC}"

# Deploy to Vercel
echo ""
echo -e "${BLUE}Deploying to Vercel...${NC}"
echo ""

vercel --prod

echo ""
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo "=================================================="
echo ""
echo -e "${BLUE}📱 Your app is now live:${NC}"
echo "   Frontend: Check Vercel dashboard for URL"
echo "   Backend: ${BACKEND_URL}"
echo "   API Docs: ${BACKEND_URL}/docs"
echo ""
echo -e "${YELLOW}⚠️  Important Next Steps:${NC}"
echo "1. Update CORS settings in backend if needed"
echo "2. Configure custom domain in Vercel dashboard"
echo "3. Set up monitoring and alerts"
echo "4. Test all features in production"
echo ""
echo -e "${GREEN}🎉 Enjoy your deployed application!${NC}"