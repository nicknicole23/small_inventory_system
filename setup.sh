#!/bin/bash

# Small Shop Inventory System - Quick Setup Script
# This script automates the setup process for both backend and frontend

echo "=================================="
echo "Small Shop Inventory System Setup"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found: $(python3 --version)${NC}"
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
echo ""

# Setup Backend
echo "=================================="
echo "Setting up Backend..."
echo "=================================="
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"

# Copy .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}Remember to update .env with your configuration${NC}"
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"
echo ""

# Go back to root
cd ..

# Setup Frontend
echo "=================================="
echo "Setting up Frontend..."
echo "=================================="
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install
echo -e "${GREEN}✓ Node.js dependencies installed${NC}"

# Copy .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
else
    echo -e "${YELLOW}.env file already exists${NC}"
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"
echo ""

# Go back to root
cd ..

# Initialize database
echo "=================================="
echo "Initializing Database..."
echo "=================================="
cd backend
source venv/bin/activate

if [ ! -d "migrations" ]; then
    echo "Initializing Flask-Migrate..."
    flask db init
    echo -e "${GREEN}✓ Flask-Migrate initialized${NC}"
    
    echo "Creating initial migration..."
    flask db migrate -m "Initial migration"
    echo -e "${GREEN}✓ Initial migration created${NC}"
    
    echo "Applying migration..."
    flask db upgrade
    echo -e "${GREEN}✓ Migration applied${NC}"
else
    echo -e "${YELLOW}Migrations folder already exists${NC}"
    echo "Run 'flask db upgrade' to apply migrations if needed"
fi

cd ..

# Summary
echo ""
echo "=================================="
echo "Setup Complete! 🎉"
echo "=================================="
echo ""
echo "To start the development servers:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open your browser to:"
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:5000"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
