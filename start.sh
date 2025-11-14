#!/bin/bash

# Small Shop Inventory System - Development Server Starter
# This script starts both backend and frontend servers

echo "Starting Small Shop Inventory System..."
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start Backend
echo "Starting Backend Server..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start Frontend
echo "Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=================================="
echo "Servers are running!"
echo "=================================="
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo "=================================="
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for all background processes
wait
