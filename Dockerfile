# syntax=docker/dockerfile:1

# --- base -------------------------------------------------------------------
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY backend ./backend
RUN pip install --upgrade pip && pip install --no-cache-dir -e .

# --- api --------------------------------------------------------------------
FROM base AS api
EXPOSE 8000
# Production: no --reload; scale with --workers (see docker-compose.prod.yml).
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- worker -----------------------------------------------------------------
FROM base AS worker
# Linux containers use the default prefork pool; Windows-native runs use --pool=solo.
CMD ["celery", "-A", "backend.workers.celery_app", "worker", "--loglevel=info"]

# --- frontend ---------------------------------------------------------------
# Lean image: the Streamlit UI only needs streamlit + plotly + httpx (it talks to
# the API over HTTP and imports no backend code), so we skip the heavy core deps.
FROM python:3.12-slim AS frontend
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir "streamlit>=1.39.0" "plotly>=5.24.0" "httpx>=0.27.0"
COPY frontend ./frontend
EXPOSE 8501
CMD ["streamlit", "run", "frontend/Home.py", \
     "--server.port=8501", "--server.address=0.0.0.0", \
     "--browser.gatherUsageStats=false"]
