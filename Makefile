.PHONY: install dev lint format typecheck test up down migrate worker

install:
	pip install -e ".[dev]"

dev:
	uvicorn backend.main:app --reload

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
