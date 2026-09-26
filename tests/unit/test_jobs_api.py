"""End-to-end jobs CRUD against the in-memory SQLite app."""

from __future__ import annotations

from httpx import AsyncClient


async def test_job_crud_lifecycle(client: AsyncClient) -> None:
    # Create
    resp = await client.post(
        "/api/v1/jobs",
        json={"title": "Senior ML Engineer", "description": "Build RAG systems."},
    )
    assert resp.status_code == 201
    job = resp.json()
    job_id = job["id"]
    assert job["title"] == "Senior ML Engineer"

    # Read
    resp = await client.get(f"/api/v1/jobs/{job_id}")
    assert resp.status_code == 200
    assert resp.json()["description"] == "Build RAG systems."

    # List
    resp = await client.get("/api/v1/jobs")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # Update
    resp = await client.patch(f"/api/v1/jobs/{job_id}", json={"title": "Staff ML Engineer"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "Staff ML Engineer"

    # Delete
    resp = await client.delete(f"/api/v1/jobs/{job_id}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/v1/jobs/{job_id}")
    assert resp.status_code == 404


async def test_get_missing_job_returns_problem_json(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/jobs/00000000-0000-0000-0000-000000000000")
    assert resp.status_code == 404
    assert resp.headers["content-type"].startswith("application/problem+json")
    body = resp.json()
    assert body["status"] == 404
    assert body["title"] == "Job not found"


async def test_create_job_validation_error(client: AsyncClient) -> None:
    resp = await client.post("/api/v1/jobs", json={"title": ""})
    assert resp.status_code == 422
    assert resp.headers["content-type"].startswith("application/problem+json")
    assert "errors" in resp.json()
