# Legacy V1 Codebase (frozen reference)

This directory holds the **original handwritten V1** of the platform, preserved
verbatim for side-by-side reference during the enterprise refactor. It is **not**
part of the new application and is intentionally excluded from:

- **CI / tooling** — ruff, black, and mypy skip `legacy/` (see `pyproject.toml`).
- **Automated tests** — pytest collects only `tests/`; `legacy/` is ignored by
  default. To run a legacy script for verification, invoke it explicitly, e.g.
  `python legacy/test_day59.py`.

The new architecture lives in [`backend/`](../backend) and (later) `frontend/`.
See [`docs/refactor-blueprint.md`](../docs/refactor-blueprint.md) for the plan.

## Immutable backup

A pristine snapshot of the pre-refactor repository (before this reorganization)
is preserved on the **`v1-legacy-baseline`** branch, pushed to `origin`. That
branch is the canonical rollback point; this `legacy/` folder is the in-tree
working reference.

## Contents

- `src/` — V1 business logic (parsing, scoring, ML training, AI modules)
- `app/` — V1 Streamlit UI + Flask API stub
- `data/`, `models/`, `artifacts/` — datasets, trained models, EDA outputs
- `config.py` — V1 configuration (kept alongside so the tree stays runnable)
- `test_*.py`, `testday3.py` — the original day-by-day test journal
- `notes/` — build notes
