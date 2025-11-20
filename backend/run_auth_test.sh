#!/bin/bash

# Script to run Flask server and authentication tests

echo "=================================="
echo "Running Authentication Tests"
echo "=================================="
echo ""

cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Check if server is already running
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Flask server is already running on port 5000"
    echo ""
    echo "Running tests..."
    python test_auth.py
else
    echo "Starting Flask server..."
    python app.py &
    SERVER_PID=$!
    
    echo "Waiting for server to start..."
    sleep 3
    
    echo ""
    echo "Running tests..."
    python test_auth.py
    
    echo ""
    echo "Stopping server..."
    kill $SERVER_PID 2>/dev/null
fi

echo ""
echo "=================================="
echo "✅ Tests Complete!"
echo "=================================="
