"""Recruiter copilot: grounded Q&A over candidate context."""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from backend.core.ports.llm import LLMProvider

SYSTEM_PROMPT = (
    "You are a recruiting copilot. Answer the recruiter's question using only the "
    "provided candidate context. Be concise and cite candidates by name. If the "
    "context is insufficient, say so rather than inventing details."
)


class CopilotService:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    async def answer(self, question: str, candidates: list[dict[str, Any]]) -> str:
        return await self._llm.generate(self._prompt(question, candidates), system=SYSTEM_PROMPT)

    async def answer_stream(
        self, question: str, candidates: list[dict[str, Any]]
    ) -> AsyncIterator[str]:
        async for chunk in self._llm.stream(
            self._prompt(question, candidates), system=SYSTEM_PROMPT
        ):
            yield chunk

    def _prompt(self, question: str, candidates: list[dict[str, Any]]) -> str:
        context = self._build_context(candidates)
        return f"CANDIDATE CONTEXT:\n{context}\n\nQUESTION: {question}"

    @staticmethod
    def _build_context(candidates: list[dict[str, Any]]) -> str:
        if not candidates:
            return "(no candidates selected)"
        parts = []
        for c in candidates:
            parts.append(
                f"- {c.get('name') or 'Unknown'} ({c.get('email') or 'no email'}): "
                f"{c.get('profile', {})}"
            )
        return "\n".join(parts)
