#!/bin/bash

# A2A System Startup Script
# Starts custom registry, agents, and Streamlit app

echo "🚀 Starting A2A System with Custom Registry..."
echo "=============================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down A2A system..."
    kill $(jobs -p) 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Start custom agent registry
echo "📋 Starting Custom Agent Registry (port 8000)..."
python3 ../registry/agent_registry.py &
REGISTRY_PID=$!
sleep 3

# Start weather agent
echo "🌤️  Starting Weather Agent (port 8080)..."
python3 ../agents/weather_agent.py --registry http://localhost:8000 &
WEATHER_PID=$!
sleep 2

# Start booking agent
echo "🏨 Starting Booking Agent (port 8081)..."
python3 ../agents/booking_agent.py --registry http://localhost:8000 &
BOOKING_PID=$!
sleep 2

# Start Streamlit app
echo "🌐 Starting Streamlit App..."
echo "   App will open at: http://localhost:8501"
echo "   Registry API at: http://localhost:8000"
echo ""
echo "✅ All services started!"
echo "🛑 Press Ctrl+C to stop all services"
echo ""

streamlit ../run ui/streamlit_app.py

# If streamlit exits, cleanup
cleanup