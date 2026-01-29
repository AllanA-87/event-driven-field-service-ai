#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

echo "Starting backend..."
cd "$ROOT/backend"
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

echo "Starting UI..."
cd "$ROOT/ui"
# Streamlit sometimes prompts for email on first run; feed blank line
printf "\n" | streamlit run app.py --server.port 8501 &
UI_PID=$!

echo ""
echo "✅ Backend: http://127.0.0.1:8000/health"
echo "✅ UI:      http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop."

trap "kill $BACKEND_PID $UI_PID" INT
wait

