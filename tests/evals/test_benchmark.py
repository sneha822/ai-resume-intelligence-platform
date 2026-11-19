"""Validate the labeled role/resume benchmark + (gated) retrieval run."""

from __future__ import annotations

import os

import pytest

from backend.eval.benchmark import evaluate_retrieval, load_benchmark, relevant_by_role


def test_benchmark_integrity() -> None:
    data = load_benchmark()
    role_ids = {r["id"] for r in data["roles"]}
    resume_ids = {r["id"] for r in data["resumes"]}

    # 30-50 labeled pairs, as specified.
    assert 30 <= len(data["labels"]) <= 50

    seen = set()
    for label in data["labels"]:
        assert label["role_id"] in role_ids
        assert label["resume_id"] in resume_ids
        assert label["label"] in {"strong", "moderate", "weak"}
        key = (label["role_id"], label["resume_id"])
        assert key not in seen, f"duplicate label {key}"
        seen.add(key)

    # Every role has at least one relevant resume to retrieve.
    rel = relevant_by_role(data)
    for rid in role_ids:
        assert rel.get(rid), f"role {rid} has no relevant resumes"


@pytest.mark.skipif(
    os.getenv("RUN_MODEL_EVALS") != "1",
    reason="Set RUN_MODEL_EVALS=1 to run the benchmark with real fastembed embeddings.",
)
async def test_hybrid_benchmark_quality() -> None:
    from backend.adapters.embeddings.fastembed_embedder import FastEmbedEmbedder

    results = await evaluate_retrieval(FastEmbedEmbedder())
    # Hybrid should retrieve most relevant candidates in the top 5.
    assert results["hybrid"]["recall@5"] >= 0.6
    assert results["hybrid"]["MRR"] >= 0.7
