"""Information-retrieval metrics for the evaluation gate.

Pure, dependency-free implementations so they run in CI without an LLM, GPU, or
external services. Used to detect retrieval-quality regressions (drift).
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence


def recall_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float:
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0
    hits = sum(1 for doc in retrieved[:k] if doc in relevant_set)
    return hits / len(relevant_set)


def precision_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float:
    if k <= 0:
        return 0.0
    relevant_set = set(relevant)
    hits = sum(1 for doc in retrieved[:k] if doc in relevant_set)
    return hits / k


def reciprocal_rank(retrieved: Sequence[str], relevant: Iterable[str]) -> float:
    relevant_set = set(relevant)
    for index, doc in enumerate(retrieved, start=1):
        if doc in relevant_set:
            return 1.0 / index
    return 0.0


def average_precision(retrieved: Sequence[str], relevant: Iterable[str]) -> float:
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0
    hits = 0
    score = 0.0
    for index, doc in enumerate(retrieved, start=1):
        if doc in relevant_set:
            hits += 1
            score += hits / index
    return score / len(relevant_set)


def ndcg_at_k(retrieved: Sequence[str], relevant: Iterable[str], k: int) -> float:
    relevant_set = set(relevant)
    dcg = 0.0
    for index, doc in enumerate(retrieved[:k], start=1):
        if doc in relevant_set:
            dcg += 1.0 / math.log2(index + 1)
    ideal_hits = min(len(relevant_set), k)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, ideal_hits + 1))
    return dcg / idcg if idcg > 0 else 0.0


def mean_reciprocal_rank(
    cases: Iterable[tuple[Sequence[str], Iterable[str]]],
) -> float:
    scores = [reciprocal_rank(r, rel) for r, rel in cases]
    return sum(scores) / len(scores) if scores else 0.0


def mean_average_precision(
    cases: Iterable[tuple[Sequence[str], Iterable[str]]],
) -> float:
    scores = [average_precision(r, rel) for r, rel in cases]
    return sum(scores) / len(scores) if scores else 0.0
