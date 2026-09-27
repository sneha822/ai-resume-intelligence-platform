"""In-memory BM25 sparse retriever (rank-bm25).

Suitable for dev-scale corpora. For very large pools this would move to a
Postgres full-text index behind the same interface.
"""

from __future__ import annotations

import re

from rank_bm25 import BM25Okapi

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class Bm25Retriever:
    """Implements the ``SparseRetriever`` protocol."""

    def __init__(self, corpus: dict[str, str]) -> None:
        self._ids = list(corpus)
        tokenized = [_tokenize(corpus[doc_id]) for doc_id in self._ids]
        self._bm25 = BM25Okapi(tokenized) if tokenized else None

    def search(self, query: str, top_k: int = 20) -> list[str]:
        if self._bm25 is None:
            return []
        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self._ids[i] for i in ranked[:top_k] if scores[i] > 0]
