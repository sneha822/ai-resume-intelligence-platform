"""Evaluation repository."""

from __future__ import annotations

import uuid

from sqlalchemy import select

from backend.db.models import Evaluation
from backend.db.repositories.base import BaseRepository


class EvaluationRepository(BaseRepository[Evaluation]):
    model = Evaluation

    async def for_job(self, job_id: uuid.UUID) -> list[Evaluation]:
        result = await self.session.execute(
            select(Evaluation)
            .where(Evaluation.job_id == job_id)
            .order_by(Evaluation.overall_score.desc())
        )
        return list(result.scalars().all())
