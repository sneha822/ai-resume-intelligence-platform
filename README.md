# AI Resume Intelligence & Interview Copilot

An enterprise-grade platform for recruiting teams: ingest resumes, search a candidate
pool with hybrid semantic + keyword retrieval, score candidates against a job with an
LLM rubric, and chat with a grounded recruiting copilot — all behind a FastAPI backend
with a Streamlit frontend.

> **Architecture:** Domain-Driven, ports & adapters. The core depends only on abstract
> **ports**; concrete **adapters** (LLM providers, embedder, parser, vector store) are
> swapped by configuration. Switching the LLM from Claude to Gemini to a local model is
> a one-line `.env` change.

---

## Demo

| Dashboard | Candidate deep-dive (competency radar + scorecard) | Hybrid search |
|---|---|---|
| ![Dashboard](docs/images/dashboard.png) | ![Deep dive](docs/images/candidate-deep-dive.png) | ![Search](docs/images/search.png) |

<!-- Live demo: add your Render/Streamlit URL here once deployed. -->
<!-- To capture the images above, see docs/images/README.md (run the app on seeded data). -->

---

## Features

- **Async resume ingestion** — PDF/text parsing (PyMuPDF), identity/attribute extraction
  (LLM structured output, with a regex/heuristic fallback), embedding, and indexing.
- **Hybrid search** — dense vectors (pgvector) + BM25, fused with Reciprocal Rank Fusion.
- **Rubric evaluation** — multi-criteria scoring (Technical / Domain / Experience /
  Leadership) with chain-of-thought reasoning, returned as validated structured output.
  Single and **bulk/batch** evaluation.
- **Recruiting copilot** — grounded Q&A over candidate context, with **SSE streaming**.
- **Multi-provider LLM** — Anthropic (Claude), Google (Gemini), or local Ollama.
- **Resilience** — Tenacity retries, a token-bucket rate limiter, and a circuit breaker
  around LLM calls; graceful degradation (partial batches, in-band stream errors).
- **Observability** — OpenTelemetry traces with per-call token/cost/latency spans.
- **Frontend** — Streamlit dashboard: search, candidate deep-dive (competency radar,
  interview scorecard, side-by-side compare), jobs, and a streaming copilot chat.
- **Quality gates** — ruff, black, mypy (strict), pytest, and retrieval/scoring
  evaluation drift gates.

---

## Architecture

```
                 ┌──────────────┐        HTTP        ┌───────────────────────────┐
                 │  Streamlit   │  ───────────────▶  │        FastAPI API        │
                 │  frontend/   │                    │        backend/api        │
                 └──────────────┘                    └────────────┬──────────────┘
                                                                  │  (DI: deps.py)
                                    ┌─────────────────────────────┼───────────────────────┐
                                    ▼                             ▼                        ▼
                            services/ (use-cases)          core/ports (Protocols)    db/ (SQLAlchemy)
                    ingestion · retrieval · evaluation      LLMProvider · Embedder    repositories
                    batch · copilot · extraction            VectorStore · Parser      Postgres+pgvector
                                    │                             ▲
                                    ▼                             │  implemented by
                            adapters/ ── llm (anthropic│gemini│ollama, resilient)
                                        ── embeddings (fastembed/ONNX)
                                        ── parsing (PyMuPDF)
                                        ── vectorstore (pgvector)
                                        ── retrieval (BM25)

  workers/  Celery + Redis (async ingest / batch)      observability/  OpenTelemetry
```

**Layout** (`backend/`):

| Package | Responsibility |
|---|---|
| `core/ports` | Abstract interfaces (`LLMProvider`, `Embedder`, `VectorStore`, `DocumentParser`) |
| `core/schemas` | Pydantic v2 I/O + LLM structured-output contracts |
| `core/resiliency` | Token-bucket rate limiter, circuit breaker |
| `services` | Use-cases: ingestion, retrieval, evaluation, batch, copilot, extraction |
| `adapters` | Concrete implementations of the ports |
| `api/v1` | FastAPI routers + DI + RFC-7807 errors |
| `db` | SQLAlchemy 2.0 (async) models, repositories, Alembic migrations |
| `workers` | Celery app + tasks |
| `observability` | OpenTelemetry setup + LLM span helpers |
| `eval` | IR metrics for the evaluation drift gates |

The original V1 codebase is preserved under `legacy/` (and on the `v1-legacy-baseline` branch).

---

## Quickstart

### 1. Prerequisites
- Python 3.10+ (developed/verified on 3.12)
- Postgres with the **pgvector** extension, and Redis — via Docker, or managed
  (e.g. Neon + Upstash)

### 2. Install
```bash
python -m venv .venv
.venv/Scripts/python -m pip install -e ".[dev]"      # backend + dev tools
# Frontend deps are kept in a separate venv to avoid resolver conflicts:
python -m venv .venv-ui
.venv-ui/Scripts/python -m pip install -e ".[frontend]"
```

### 3. Configure
```bash
cp .env.example .env
# then edit .env — see "Configuration" below
```

### 4. Infra + migrations
```bash
docker compose up -d postgres redis     # or point DATABASE_URL/REDIS_URL at managed services
.venv/Scripts/python -m alembic upgrade head
```

### 5. Run
```bash
# API (use `python -m backend` on Windows — sets the SelectorEventLoop for async psycopg)
.venv/Scripts/python -m backend                       # http://127.0.0.1:8000

# Celery worker (Windows requires --pool=solo)
.venv/Scripts/celery -A backend.workers.celery_app worker --loglevel=info --pool=solo

# Frontend
AIRI_API_URL=http://127.0.0.1:8000 .venv-ui/Scripts/python -m streamlit run frontend/Home.py
```

Open the API docs at `http://127.0.0.1:8000/docs` and the UI at `http://localhost:8501`.

---

## Configuration

Key `.env` settings (full list in `.env.example`):

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | `postgresql+psycopg://…` (managed Postgres, e.g. Neon: append `?sslmode=require&channel_binding=disable`) |
| `REDIS_URL` / `CELERY_*` | Redis broker/backend (managed, e.g. Upstash: `rediss://…?ssl_cert_reqs=required`) |
| `LLM_PROVIDER` | `anthropic` \| `gemini` \| `ollama` |
| `ANTHROPIC_API_KEY` / `LLM_MODEL` | Claude (e.g. `claude-sonnet-5`) |
| `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) / `GEMINI_MODEL` | Gemini (e.g. `gemini-3.8-flash`) |
| `OLLAMA_MODEL` | Local model when `LLM_PROVIDER=ollama` |
| `EMBEDDING_MODEL` / `EMBEDDING_DIM` | fastembed ONNX model (default `BAAI/bge-base-en-v1.5`, 768) |
| `OTEL_ENABLED` / `OTEL_EXPORTER_OTLP_ENDPOINT` | OpenTelemetry (point at Phoenix/any OTLP collector) |

### LLM providers
The active provider is chosen by `LLM_PROVIDER`; all LLM features work on any of them.
- **Anthropic** — Claude via Instructor for schema-validated structured output.
- **Gemini** — google-genai with native `response_schema` structured output.
  Note: some model ids retire (e.g. `gemini-2.5-flash` → use `gemini-3.8-flash`).
- **Ollama** — fully local/offline; JSON-mode structured output validated by Pydantic.

If no provider key is configured, LLM endpoints return `503`; retrieval and CRUD still work.

---

## API (v1)

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/resumes` | Upload a resume (async ingest → `202` + `task_id`) |
| `GET` | `/api/v1/resumes/tasks/{id}` | Ingestion task status |
| `POST` | `/api/v1/search` | Hybrid RRF candidate search |
| `GET` | `/api/v1/candidates` · `/{id}` | List / deep-dive (resumes, evaluations) |
| `POST` | `/api/v1/jobs` · CRUD | Manage job postings |
| `POST` | `/api/v1/evaluations` | Single rubric evaluation |
| `POST` | `/api/v1/evaluations/batch` | Bulk evaluation (partial-result tolerant) |
| `POST` | `/api/v1/copilot` · `/copilot/stream` | Grounded Q&A (JSON or SSE stream) |
| `GET` | `/health` · `/ready` | Liveness / readiness |

---

## Development

```bash
.venv/Scripts/ruff check backend frontend tests
.venv/Scripts/black --check backend frontend tests
.venv/Scripts/mypy backend
.venv/Scripts/python -m pytest
```

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for production deployment (Docker
Compose, managed services, and Kubernetes), including the `docker-compose.prod.yml`
overrides, migrations, scaling, and a security checklist. A full walkthrough of the
concepts, decisions, and Q&A is in **[docs/INTERVIEW_PREP.md](docs/INTERVIEW_PREP.md)**.

Tests that need infrastructure are skipped by default; enable them with env flags:
- `RUN_DB_TESTS=1` — repository + pgvector integration tests (needs live Postgres)
- `RUN_MODEL_EVALS=1` — retrieval drift gate with real fastembed embeddings
- `RUN_LLM_EVALS=1` — scoring drift gate (needs a configured LLM)

CI (`.github/workflows/ci.yml`) runs ruff, black, mypy, and pytest on every push/PR.

---

## Tech stack

FastAPI · SQLAlchemy 2.0 (async) + Alembic · Postgres + pgvector · Pydantic v2 ·
Celery + Redis · fastembed (ONNX) · rank-bm25 · PyMuPDF · Anthropic / google-genai /
Ollama · OpenTelemetry · Streamlit + Plotly · ruff / black / mypy / pytest.
