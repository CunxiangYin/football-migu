#!/bin/bash

# Script to help push code to GitHub
# Usage: ./push-to-github.sh [username] [repo-name]

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}📤 Push to GitHub Helper${NC}"
echo "========================"

# Get GitHub username
if [ -z "$1" ]; then
    echo -e "${YELLOW}Enter your GitHub username:${NC}"
    read GITHUB_USER
else
    GITHUB_USER=$1
fi

# Get repository name
if [ -z "$2" ]; then
    REPO_NAME="football-migu"
    echo -e "${YELLOW}Repository name (default: football-migu):${NC}"
    read INPUT_REPO
    if [ ! -z "$INPUT_REPO" ]; then
        REPO_NAME=$INPUT_REPO
    fi
else
    REPO_NAME=$2
fi

echo ""
echo -e "${GREEN}Configuration:${NC}"
echo "  Username: $GITHUB_USER"
echo "  Repository: $REPO_NAME"
echo ""

# Check if remote already exists
if git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}Remote 'origin' already exists. Do you want to update it? (y/n)${NC}"
    read RESPONSE
    if [ "$RESPONSE" = "y" ]; then
        git remote remove origin
    else
        echo "Using existing remote."
    fi
fi

# Add remote if not exists
if ! git remote get-url origin >/dev/null 2>&1; then
    echo -e "${YELLOW}Use HTTPS or SSH? (https/ssh):${NC}"
    read PROTOCOL
    
    if [ "$PROTOCOL" = "ssh" ]; then
        REMOTE_URL="git@github.com:${GITHUB_USER}/${REPO_NAME}.git"
    else
        REMOTE_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
    fi
    
    echo "Adding remote: $REMOTE_URL"
    git remote add origin $REMOTE_URL
fi

# Set main branch
git branch -M main

echo ""
echo -e "${GREEN}Ready to push!${NC}"
echo -e "${YELLOW}Make sure you have created the repository on GitHub first!${NC}"
echo ""
echo "Commands to run:"
echo "  git push -u origin main"
echo ""
echo -e "${YELLOW}Do you want to push now? (y/n)${NC}"
read PUSH_NOW

if [ "$PUSH_NOW" = "y" ]; then
    echo "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
        echo ""
        echo "Your repository is now available at:"
        echo "  https://github.com/${GITHUB_USER}/${REPO_NAME}"
        echo ""
        echo "Next steps:"
        echo "  1. Add a description and topics on GitHub"
        echo "  2. Configure GitHub Pages if needed"
        echo "  3. Set up GitHub Actions for CI/CD"
        echo "  4. Add collaborators if working in a team"
    else
        echo ""
        echo -e "${RED}❌ Push failed. Please check:${NC}"
        echo "  1. Have you created the repository on GitHub?"
        echo "  2. Do you have the correct permissions?"
        echo "  3. Is your authentication configured?"
        echo ""
        echo "For HTTPS, you may need a Personal Access Token:"
        echo "  https://github.com/settings/tokens"
        echo ""
        echo "For SSH, make sure your SSH key is added:"
        echo "  https://github.com/settings/keys"
    fi
else
    echo ""
    echo "You can push manually with:"
    echo "  git push -u origin main"
fi