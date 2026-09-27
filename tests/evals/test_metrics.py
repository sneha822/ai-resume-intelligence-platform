"""Unit tests for the IR metrics (always run, deterministic)."""

from __future__ import annotations

import pytest

from backend.eval.metrics import (
    average_precision,
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_and_precision() -> None:
    retrieved = ["a", "x", "b", "y"]
    relevant = {"a", "b", "c"}
    assert recall_at_k(retrieved, relevant, k=4) == pytest.approx(2 / 3)
    assert precision_at_k(retrieved, relevant, k=4) == pytest.approx(2 / 4)


def test_reciprocal_rank() -> None:
    assert reciprocal_rank(["x", "a"], {"a"}) == pytest.approx(0.5)
    assert reciprocal_rank(["x", "y"], {"a"}) == 0.0


def test_average_precision() -> None:
    # relevant at ranks 1 and 3 -> (1/1 + 2/3) / 2
    assert average_precision(["a", "x", "b"], {"a", "b"}) == pytest.approx((1.0 + 2 / 3) / 2)


def test_ndcg_perfect_is_one() -> None:
    assert ndcg_at_k(["a", "b", "x"], {"a", "b"}, k=3) == pytest.approx(1.0)


def test_mrr_average() -> None:
    cases = [(["a"], {"a"}), (["x", "b"], {"b"})]
    assert mean_reciprocal_rank(cases) == pytest.approx((1.0 + 0.5) / 2)
