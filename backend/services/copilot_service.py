"""Recruiter copilot: grounded Q&A over candidate context."""

from __future__ import annotations

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
        context = self._build_context(candidates)
        prompt = f"CANDIDATE CONTEXT:\n{context}\n\nQUESTION: {question}"
        return await self._llm.generate(prompt, system=SYSTEM_PROMPT)

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
