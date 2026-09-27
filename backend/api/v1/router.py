"""Aggregate v1 API router."""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.v1 import candidates, copilot, evaluations, jobs, resumes, search

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(jobs.router)
api_router.include_router(candidates.router)
api_router.include_router(resumes.router)
api_router.include_router(search.router)
api_router.include_router(evaluations.router)
api_router.include_router(copilot.router)
