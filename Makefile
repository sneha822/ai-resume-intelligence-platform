.PHONY: install dev lint format typecheck test up down migrate worker ui

install:
	pip install -e ".[dev]"

# Windows-safe launcher (sets SelectorEventLoop for async psycopg).
# On Linux/Docker `uvicorn backend.main:app` also works.
dev:
	python -m backend

lint:
	ruff check backend frontend tests

format:
	black backend frontend tests
	ruff check --fix backend frontend tests

ui:
	streamlit run frontend/Home.py

typecheck:
	mypy backend

test:
	pytest

up:
	docker compose up -d --build

down:
	docker compose down

# Windows-native worker (solo pool required)
worker:
	celery -A backend.workers.celery_app worker --loglevel=info --pool=solo
