# syntax=docker/dockerfile:1

# --- base -------------------------------------------------------------------
FROM python:3.10-slim AS base
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY backend ./backend
RUN pip install --upgrade pip && pip install -e .

# --- api --------------------------------------------------------------------
FROM base AS api
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- worker -----------------------------------------------------------------
FROM base AS worker
# Linux containers use the default prefork pool; Windows-native runs use --pool=solo
CMD ["celery", "-A", "backend.workers.celery_app", "worker", "--loglevel=info"]
