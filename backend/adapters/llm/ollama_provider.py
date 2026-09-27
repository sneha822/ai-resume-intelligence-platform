"""Ollama LLM provider for local/offline use.

Structured output is achieved by requesting JSON and validating it against the
Pydantic ``response_model`` (retrying on validation failure), preserving the
"guaranteed valid model" contract without a hosted API.
"""

from __future__ import annotations

from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.core.config import settings

T = TypeVar("T", bound=BaseModel)

_RETRY = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True,
)


class OllamaProvider:
    def __init__(self, model: str | None = None, host: str = "http://localhost:11434"):
        self._model = model or settings.ollama_model
        self._host = host

    async def _call(self, prompt: str, system: str | None, fmt_json: bool) -> str:
        payload: dict[str, object] = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
        }
        if system:
            payload["system"] = system
        if fmt_json:
            payload["format"] = "json"
        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(f"{self._host}/api/generate", json=payload)
            resp.raise_for_status()
            data = resp.json()
        return str(data.get("response", ""))

    @_RETRY
    async def generate(self, prompt: str, system: str | None = None) -> str:
        return await self._call(prompt, system, fmt_json=False)

    @_RETRY
    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        raw = await self._call(prompt, system, fmt_json=True)
        try:
            return response_model.model_validate_json(raw)
        except ValidationError as exc:
            raise ValueError(f"Ollama returned invalid data for {response_model.__name__}") from exc
