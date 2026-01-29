#!/usr/bin/env bash
cd /Users/allanarguello/ai-ops-copilot/backend
source .venv/bin/activate
cd ../ui
printf "\n" | streamlit run app.py --server.port 8501

