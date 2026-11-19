"""Labeled role/resume benchmark: loader + retrieval evaluation.

The dataset (``role_resume_pairs.json``) is a small hand-labeled set of
(role, resume) relevance judgments (strong / moderate / weak) over synthetic
resumes. Use it to compute retrieval quality (dense vs sparse vs hybrid) with the
metrics in ``backend.eval.metrics``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from backend.adapters.retrieval.bm25 import Bm25Retriever
from backend.core.ports.embedder import Embedder
from backend.eval.metrics import (
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)

_DATA_PATH = Path(__file__).parent / "role_resume_pairs.json"

# Which labels count as "relevant" for binary retrieval metrics.
_RELEVANT_LABELS = {"strong", "moderate"}


def load_benchmark() -> dict[str, Any]:
    with _DATA_PATH.open(encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    return data


def relevant_by_role(data: dict[str, Any]) -> dict[str, set[str]]:
    """role_id -> set of resume_ids judged relevant (strong or moderate)."""
    out: dict[str, set[str]] = {}
    for label in data["labels"]:
        if label["label"] in _RELEVANT_LABELS:
            out.setdefault(label["role_id"], set()).add(label["resume_id"])
    return out


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def _rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank + 1)
    return [d for d, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]


async def evaluate_retrieval(embedder: Embedder) -> dict[str, dict[str, float]]:
    """Run dense/sparse/hybrid retrieval over the benchmark; return metrics per method."""
    data = load_benchmark()
    resumes = data["resumes"]
    corpus = {r["id"]: r["text"] for r in resumes}
    ids = list(corpus)
    relevant = relevant_by_role(data)

    corpus_vecs = {rid: (await embedder.embed(corpus[rid])) for rid in ids}
    bm25 = Bm25Retriever(corpus)

    cases: dict[str, list[tuple[list[str], set[str]]]] = {
        "dense": [],
        "sparse": [],
        "hybrid": [],
    }
    for role in data["roles"]:
        rel = relevant.get(role["id"], set())
        if not rel:
            continue
        qv = await embedder.embed(role["description"])
        dense = [
            rid
            for rid, _ in sorted(
                ((rid, _cosine(qv, corpus_vecs[rid])) for rid in ids),
                key=lambda x: x[1],
                reverse=True,
            )
        ]
        sparse = bm25.search(role["description"], top_k=len(ids))
        hybrid = _rrf([dense, sparse])
        cases["dense"].append((dense, rel))
        cases["sparse"].append((sparse, rel))
        cases["hybrid"].append((hybrid, rel))

    def metrics(pairs: list[tuple[list[str], set[str]]]) -> dict[str, float]:
        n = len(pairs)
        return {
            "recall@3": sum(recall_at_k(r, rel, 3) for r, rel in pairs) / n,
            "recall@5": sum(recall_at_k(r, rel, 5) for r, rel in pairs) / n,
            "precision@3": sum(precision_at_k(r, rel, 3) for r, rel in pairs) / n,
            "MRR": mean_reciprocal_rank(pairs),
            "nDCG@5": sum(ndcg_at_k(r, rel, 5) for r, rel in pairs) / n,
        }

    return {method: metrics(pairs) for method, pairs in cases.items()}
