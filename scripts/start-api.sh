#!/usr/bin/env sh
# Start the API: run DB migrations, then serve on Render's $PORT (default 8000).
set -e
alembic upgrade head
exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
