"""Thin HTTP client around the FastAPI backend.

The frontend holds no business logic; every action is an API call.
"""

from __future__ import annotations

import contextlib
import os
from collections.abc import Iterator
from typing import Any

import httpx

DEFAULT_BASE_URL = os.getenv("AIRI_API_URL", "http://127.0.0.1:8000")


class APIError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        super().__init__(f"{status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail


class APIClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: float = 60.0) -> None:
        self._base = base_url.rstrip("/")
        self._api = f"{self._base}/api/v1"
        self._timeout = timeout

    def _request(self, method: str, url: str, **kwargs: Any) -> Any:
        try:
            resp = httpx.request(method, url, timeout=self._timeout, **kwargs)
        except httpx.RequestError as exc:
            raise APIError(0, f"Cannot reach API at {self._base}: {exc}") from exc
        if resp.status_code >= 400:
            detail = resp.text
            with contextlib.suppress(Exception):
                detail = resp.json().get("detail", detail)
            raise APIError(resp.status_code, str(detail))
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    # --- system ---
    def health(self) -> dict[str, Any]:
        return self._request("GET", f"{self._base}/health")

    # --- jobs ---
    def list_jobs(self) -> list[dict[str, Any]]:
        return self._request("GET", f"{self._api}/jobs")

    def create_job(self, title: str, description: str) -> dict[str, Any]:
        return self._request(
            "POST", f"{self._api}/jobs", json={"title": title, "description": description}
        )

    # --- candidates ---
    def list_candidates(self) -> list[dict[str, Any]]:
        return self._request("GET", f"{self._api}/candidates")

    def get_candidate(self, candidate_id: str) -> dict[str, Any]:
        return self._request("GET", f"{self._api}/candidates/{candidate_id}")

    # --- search ---
    def search(self, query: str, top_k: int = 10) -> list[dict[str, Any]]:
        return self._request("POST", f"{self._api}/search", json={"query": query, "top_k": top_k})

    # --- resumes ---
    def upload_resume(self, filename: str, content: bytes) -> dict[str, Any]:
        files = {"file": (filename, content, "application/pdf")}
        return self._request("POST", f"{self._api}/resumes", files=files)

    # --- evaluations ---
    def evaluate(self, candidate_id: str, job_id: str) -> dict[str, Any]:
        return self._request(
            "POST",
            f"{self._api}/evaluations",
            json={"candidate_id": candidate_id, "job_id": job_id},
        )

    def evaluate_batch(self, job_id: str, candidate_ids: list[str] | None = None) -> dict[str, Any]:
        return self._request(
            "POST",
            f"{self._api}/evaluations/batch",
            json={"job_id": job_id, "candidate_ids": candidate_ids or []},
        )

    # --- copilot ---
    def copilot(self, question: str, candidate_ids: list[str]) -> dict[str, Any]:
        return self._request(
            "POST",
            f"{self._api}/copilot",
            json={"question": question, "candidate_ids": candidate_ids},
        )

    def copilot_stream(self, question: str, candidate_ids: list[str]) -> Iterator[str]:
        """Yield answer chunks from the SSE endpoint (for st.write_stream)."""
        import json

        body = {"question": question, "candidate_ids": candidate_ids}
        try:
            with httpx.stream(
                "POST", f"{self._api}/copilot/stream", json=body, timeout=self._timeout
            ) as resp:
                if resp.status_code >= 400:
                    resp.read()
                    detail = resp.text
                    with contextlib.suppress(Exception):
                        detail = resp.json().get("detail", detail)
                    raise APIError(resp.status_code, str(detail))
                for line in resp.iter_lines():
                    if not line.startswith("data: "):
                        continue
                    payload = line[len("data: ") :]
                    if payload == "[DONE]":
                        break
                    with contextlib.suppress(Exception):
                        yield json.loads(payload).get("delta", "")
        except httpx.RequestError as exc:
            raise APIError(0, f"Cannot reach API at {self._base}: {exc}") from exc
