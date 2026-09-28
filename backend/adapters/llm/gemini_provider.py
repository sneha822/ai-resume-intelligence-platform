"""Google Gemini LLM provider.

Implements the ``LLMProvider`` port using the google-genai SDK. Structured output
uses Gemini's native ``response_schema`` (Pydantic), so it returns a validated
model without a separate parsing library. Emits an OpenTelemetry span per call.
"""

from __future__ import annotations

import time
from collections.abc import AsyncIterator
from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

from backend.core.config import settings
from backend.observability.llm_tracing import set_llm_span_attributes
from backend.observability.telemetry import get_tracer

if TYPE_CHECKING:
    from google.genai import Client

T = TypeVar("T", bound=BaseModel)

_TRACER = get_tracer("backend.adapters.llm.gemini")

_RETRY = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    reraise=True,
)


class GeminiProvider:
    def __init__(self, model: str | None = None, api_key: str | None = None) -> None:
        from google.genai import Client

        self._client: Client = Client(api_key=api_key or settings.gemini_api_key)
        self._model = model or settings.gemini_model

    def _record(self, span: Any, usage: Any, started: float) -> None:
        set_llm_span_attributes(
            span,
            model=self._model,
            input_tokens=int(getattr(usage, "prompt_token_count", 0) or 0),
            output_tokens=int(getattr(usage, "candidates_token_count", 0) or 0),
            latency_seconds=time.perf_counter() - started,
            system="google",
        )

    @_RETRY
    async def generate(self, prompt: str, system: str | None = None) -> str:
        from google.genai import types

        with _TRACER.start_as_current_span("llm.generate") as span:
            started = time.perf_counter()
            config = types.GenerateContentConfig(system_instruction=system)
            response = await self._client.aio.models.generate_content(
                model=self._model, contents=prompt, config=config
            )
            self._record(span, response.usage_metadata, started)
            return response.text or ""

    @_RETRY
    async def structured(
        self, prompt: str, response_model: type[T], system: str | None = None
    ) -> T:
        from google.genai import types

        with _TRACER.start_as_current_span("llm.structured") as span:
            started = time.perf_counter()
            config = types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json",
                response_schema=response_model,
            )
            response = await self._client.aio.models.generate_content(
                model=self._model, contents=prompt, config=config
            )
            self._record(span, response.usage_metadata, started)
            parsed = response.parsed
            if isinstance(parsed, response_model):
                return parsed
            # Fallback: validate the raw JSON text.
            result: T = response_model.model_validate_json(response.text or "{}")
            return result

    async def stream(self, prompt: str, system: str | None = None) -> AsyncIterator[str]:
        from google.genai import types

        config = types.GenerateContentConfig(system_instruction=system)
        stream = await self._client.aio.models.generate_content_stream(
            model=self._model, contents=prompt, config=config
        )
        async for chunk in stream:
            if chunk.text:
                yield chunk.text
