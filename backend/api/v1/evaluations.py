"""Synchronous single-candidate evaluation endpoint.

Runs the rubric evaluator inline (through the resilient Claude provider) and
persists the result. Batch/async evaluation is handled by the Celery
``batch_evaluate`` task.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from backend.api.deps import EvaluationServiceDep, SessionDep
from backend.core.schemas import (
    BatchEvaluationItem,
    BatchEvaluationRequest,
    BatchEvaluationResponse,
    EvaluationRead,
    EvaluationRequest,
)
from backend.db.models import Evaluation
from backend.db.repositories import CandidateRepository, JobRepository
from backend.services.batch_evaluation_service import BatchEvaluationService

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("", response_model=EvaluationRead, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    payload: EvaluationRequest, session: SessionDep, service: EvaluationServiceDep
) -> Evaluation:
    candidate = await CandidateRepository(session).get(payload.candidate_id)
    if candidate is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    job = await JobRepository(session).get(payload.job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")

    result = await service.evaluate(
        candidate={
            "name": candidate.name,
            "email": candidate.email,
            "profile": candidate.profile,
        },
        job={"title": job.title, "description": job.description},
    )

    evaluation = Evaluation(
        candidate_id=candidate.id,
        job_id=job.id,
        overall_score=result.overall_score,
        fit_level=result.fit_level.value,
        result=result.model_dump(mode="json"),
    )
    session.add(evaluation)
    await session.commit()
    await session.refresh(evaluation)
    return evaluation


@router.post(
    "/batch",
    response_model=BatchEvaluationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_batch_evaluations(
    payload: BatchEvaluationRequest, session: SessionDep, service: EvaluationServiceDep
) -> BatchEvaluationResponse:
    job = await JobRepository(session).get(payload.job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")

    batch = BatchEvaluationService(session, service)
    pairs = await batch.evaluate_job(job, payload.candidate_ids or None)

    return BatchEvaluationResponse(
        job_id=job.id,
        evaluated=len(pairs),
        results=[
            BatchEvaluationItem(
                candidate_id=candidate.id,
                overall_score=result.overall_score,
                fit_level=result.fit_level.value,
            )
            for candidate, result in pairs
        ],
    )
