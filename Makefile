.PHONY: install dev lint format typecheck test up down migrate worker

install:
	pip install -e ".[dev]"

# Windows-safe launcher (sets SelectorEventLoop for async psycopg).
# On Linux/Docker `uvicorn backend.main:app` also works.
dev:
	python -m backend

lint:
	ruff check backend tests

format:
	black backend tests
	ruff check --fix backend tests

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
