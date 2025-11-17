#!/bin/bash
# Quick local testing script

set -e

echo "🧪 Testing Kinic Memory Agent Locally"
echo "======================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Copy .env.example to .env and fill in your values"
    exit 1
fi

# Load environment
export $(cat .env | grep -v '^#' | xargs)

# Check required vars
required_vars=("MONAD_RPC_URL" "MONAD_PRIVATE_KEY" "MONAD_CONTRACT_ADDRESS" "KINIC_MEMORY_ID")

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: $var not set in .env"
        exit 1
    fi
done

echo "✅ Environment variables loaded"
echo ""

# Start server in background
echo "🚀 Starting FastAPI server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping server..."
    kill $SERVER_PID 2>/dev/null || true
}
trap cleanup EXIT

# Test health endpoint
echo ""
echo "📡 Testing /health endpoint..."
curl -s http://localhost:8000/health | python -m json.tool
echo ""

# Test insert endpoint
echo ""
echo "📝 Testing /insert endpoint..."
curl -s -X POST http://localhost:8000/insert \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Test Memory\n\nThis is a test memory for the Kinic Monad agent. It demonstrates the integration between Kinic (Internet Computer) for storage and Monad blockchain for metadata logging.",
    "user_tags": "test,example"
  }' | python -m json.tool
echo ""

# Test search endpoint
echo ""
echo "🔍 Testing /search endpoint..."
curl -s -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test memory",
    "top_k": 3
  }' | python -m json.tool
echo ""

# Test stats endpoint
echo ""
echo "📊 Testing /stats endpoint..."
curl -s http://localhost:8000/stats | python -m json.tool
echo ""

echo ""
echo "✅ All tests completed!"
echo ""
echo "💡 Server is still running on http://localhost:8000"
echo "   Press Ctrl+C to stop"
echo ""
echo "📚 API docs available at http://localhost:8000/docs"

# Wait for user interrupt
wait $SERVER_PID
