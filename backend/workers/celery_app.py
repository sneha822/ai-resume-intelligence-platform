"""Celery application.

On Windows, run the worker with the solo pool::

    celery -A backend.workers.celery_app worker --loglevel=info --pool=solo

The prefork pool (Celery's default) does not work reliably on Windows, so
``--pool=solo`` is the supported local option here. Tasks are registered in
``backend.workers.tasks`` (added in Phase 6).
"""

from __future__ import annotations

from celery import Celery

from backend.core.config import settings

celery_app = Celery(
    "airi",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["backend.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,
    task_time_limit=600,
)
