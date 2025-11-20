#!/bin/bash

# Quick Setup Script for Authentication System
# Run this after creating the auth files

echo "=================================="
echo "Authentication System Setup"
echo "=================================="
echo ""

cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if migrations directory exists
if [ ! -d "migrations" ]; then
    echo ""
    echo "Initializing Flask-Migrate..."
    flask db init
fi

# Create migration for User model
echo ""
echo "Creating migration for User model..."
flask db migrate -m "Add User model for authentication"

# Apply migration
echo ""
echo "Applying migration..."
flask db upgrade

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Start the server: python app.py"
echo "2. In another terminal, run tests: python test_auth.py"
echo ""
echo "Or run: ./run_auth_test.sh (to do both)"
echo ""
