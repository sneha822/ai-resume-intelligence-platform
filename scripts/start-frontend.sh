#!/usr/bin/env sh
# Start the Streamlit frontend on Render's $PORT (default 8501).
exec streamlit run frontend/Home.py \
  --server.port "${PORT:-8501}" \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false
