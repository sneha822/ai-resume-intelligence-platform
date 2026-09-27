"""Job posting CRUD endpoints."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, status

from backend.api.deps import SessionDep
from backend.core.schemas import JobCreate, JobRead, JobUpdate
from backend.db.models import Job
from backend.db.repositories import JobRepository

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
async def create_job(payload: JobCreate, session: SessionDep) -> Job:
    repo = JobRepository(session)
    job = await repo.add(Job(title=payload.title, description=payload.description))
    await session.commit()
    await session.refresh(job)
    return job


@router.get("", response_model=list[JobRead])
async def list_jobs(session: SessionDep, limit: int = 100, offset: int = 0) -> list[Job]:
    repo = JobRepository(session)
    return await repo.list(limit=limit, offset=offset)


@router.get("/{job_id}", response_model=JobRead)
async def get_job(job_id: uuid.UUID, session: SessionDep) -> Job:
    repo = JobRepository(session)
    job = await repo.get(job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.patch("/{job_id}", response_model=JobRead)
async def update_job(job_id: uuid.UUID, payload: JobUpdate, session: SessionDep) -> Job:
    repo = JobRepository(session)
    job = await repo.get(job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    if payload.title is not None:
        job.title = payload.title
    if payload.description is not None:
        job.description = payload.description
    await session.commit()
    await session.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: uuid.UUID, session: SessionDep) -> None:
    repo = JobRepository(session)
    job = await repo.get(job_id)
    if job is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    await repo.delete(job)
    await session.commit()
