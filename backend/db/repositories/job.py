"""Job repository."""

from __future__ import annotations

from backend.db.models import Job
from backend.db.repositories.base import BaseRepository


class JobRepository(BaseRepository[Job]):
    model = Job
