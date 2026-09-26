"""Aggregate v1 API router."""

from __future__ import annotations

from fastapi import APIRouter

from backend.api.v1 import jobs, search

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(jobs.router)
api_router.include_router(search.router)
