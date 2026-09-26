# Enterprise Refactor Blueprint

**Project:** AI Resume Intelligence & Interview Copilot
**Goal:** Elevate from Streamlit-script collection to an enterprise-ready, FAANG-grade AI/ML product.
**Decisions locked:** Vector store = **pgvector** (reuse Postgres) · LLM stack = **Claude + Instructor** (Ollama kept for offline) · Structured output enforced via **Pydantic v2 + Instructor**.

---

## 0. Current State (grounding)

| Area | Today | Gap |
|---|---|---|
| API | 43-line Flask stub (`app/api.py`) that echoes JSON | Not wired to real logic |
| UI | 554-line monolithic Streamlit (`app/app.py`) importing `src.*` directly | UI ↔ logic tightly coupled |
| AI layer | `src/ai/` package: `V2RecruitingPipeline`, `LLMClient` (Ollama/llama3.2), `hybrid_parser`, `candidate_evaluator`, `candidate_knowledge`, `candidate_search`, `copilot` | Solid base; needs contracts + real retrieval |
| Schemas | `src/ai/schemas.py` uses `@dataclass`; parsing via `json.loads(response)` | No structured-output guarantee — biggest reliability gap |
| Persistence | raw `sqlite3`, 4-column table (`id, email, phone, skills`) | No ORM, no migrations, no audit trail |
| Vector search | none (`candidate_knowledge` is not a real vector store) | Need hybrid BM25 + dense + RRF |
| Tests | ~70 `test_dayN.py` in repo root (a journal) | Not a real `tests/` suite |
| Scoring | TF-IDF / token intersection (`src/scoring.py`, `match_scorer.py`) | Keep as BM25/sparse leg only |

**Strategy: consolidate + elevate, not rewrite.** The `src/ai/` layer is a real head start.

---

## 1. Target Directory Structure

```
ai-resume-intelligence-platform/
├── pyproject.toml                  # replaces requirements.txt; ruff, black, mypy, pytest config
├── docker-compose.yml              # api, worker, postgres(+pgvector), redis, ui
├── Dockerfile                      # multi-stage: base → api → worker
├── Makefile                        # make dev / test / lint / migrate
├── .env.example
├── alembic.ini
│
├── backend/
│   ├── main.py                     # FastAPI app factory + lifespan
│   ├── api/
│   │   ├── deps.py                 # DI: db session, current_user, settings
│   │   ├── errors.py               # exception handlers → RFC 7807 problem+json
│   │   └── v1/
│   │       ├── router.py           # aggregates routers
│   │       ├── resumes.py          # POST /resumes (async ingest), GET /resumes/{id}
│   │       ├── jobs.py             # CRUD job postings
│   │       ├── search.py           # hybrid + NL search
│   │       ├── evaluations.py      # rubric evaluation, gap analysis
│   │       └── copilot.py          # streaming chat (SSE)
│   │
│   ├── core/                       # framework-agnostic domain (no FastAPI/SQLAlchemy imports)
│   │   ├── config.py               # pydantic-settings BaseSettings
│   │   ├── domain/                 # entities: Candidate, Job, Evaluation, Match
│   │   ├── schemas/                # Pydantic I/O + LLM structured-output models
│   │   │   ├── candidate.py
│   │   │   ├── evaluation.py       # RubricScore, EvaluationResult, GapAnalysis
│   │   │   └── search.py
│   │   └── ports/                  # abstract interfaces (Protocols)
│   │       ├── llm.py              # LLMProvider
│   │       ├── vector_store.py     # VectorStore
│   │       ├── embedder.py         # Embedder
│   │       └── parser.py           # DocumentParser
│   │
│   ├── services/                   # use-cases orchestrating ports + repos
│   │   ├── ingestion_service.py
│   │   ├── retrieval_service.py    # hybrid search + RRF
│   │   ├── evaluation_service.py   # rubric evaluator + CoT
│   │   └── copilot_service.py
│   │
│   ├── adapters/                   # concrete implementations of ports
│   │   ├── llm/
│   │   │   ├── anthropic_provider.py   # Claude + instructor
│   │   │   └── ollama_provider.py      # existing local path
│   │   ├── parsing/docling_parser.py   # or unstructured/llamaparse
│   │   ├── embeddings/bge_embedder.py  # bge-large-en-v1.5 (local) / voyage
│   │   └── vectorstore/pgvector_store.py
│   │
│   ├── db/
│   │   ├── base.py                 # DeclarativeBase, engine, sessionmaker
│   │   ├── models.py               # SQLAlchemy 2.0 ORM (Mapped[...]) incl. Vector column
│   │   ├── repositories/           # CandidateRepo, JobRepo, EvaluationRepo
│   │   └── migrations/             # alembic versions (enable `vector` extension in baseline)
│   │
│   ├── workers/
│   │   ├── celery_app.py
│   │   └── tasks.py                # ingest_resume, batch_evaluate, reindex
│   │
│   └── observability/
│       ├── telemetry.py            # OpenTelemetry setup
│       └── llm_tracing.py          # Phoenix / LangSmith hooks
│
├── frontend/                       # Streamlit overhaul (thin HTTP client only)
│   ├── Home.py
│   ├── pages/1_Search.py  2_Candidate_Deep_Dive.py  3_Copilot.py  4_Compare.py
│   ├── components/                 # cards, radar_chart, scorecard, chat
│   ├── api_client.py               # httpx wrapper around backend
│   └── theme/tokens.py             # CSS tokens, dark mode
│
├── tests/
│   ├── unit/  integration/  evals/  # evals/ = Ragas/DeepEval retrieval+scoring drift
│   └── conftest.py                 # fixtures: test db, fake LLM, testcontainers
│
├── legacy/                         # entire V1 codebase (src/, app/, data/, ...) kept as reference, excluded from CI
└── .github/workflows/ci.yml
```

---

## 2. Migration Map

| Current | Destination | Change |
|---|---|---|
| `app/api.py` (Flask) | `backend/api/v1/*` | Rewrite in FastAPI, wire to services |
| `app/app.py` (554 LOC) | `frontend/` | Split into pages/components; HTTP-only, no `src` imports |
| `src/ai/llm_client.py` | `backend/adapters/llm/*` | Split into `LLMProvider` port + Ollama/Anthropic adapters |
| `src/ai/schemas.py` (dataclasses) | `backend/core/schemas/*` | Convert to **Pydantic v2** |
| `src/ai/candidate_evaluator.py` | `backend/services/evaluation_service.py` | Add rubric + `instructor` structured output |
| `src/ai/candidate_knowledge.py` + `candidate_search.py` | `backend/services/retrieval_service.py` + `adapters/vectorstore` | Real hybrid search + RRF |
| `src/ai/hybrid_parser.py` | `backend/adapters/parsing/*` | Wrap Docling/Unstructured |
| `src/database.py` (sqlite3) | `backend/db/*` | SQLAlchemy 2.0 + Alembic + Postgres/pgvector |
| `src/scoring.py`, `match_scorer.py`, TF-IDF | `retrieval_service` (BM25 leg) | Keep as sparse signal, drop as final scorer |
| `test_day*.py` + all V1 code (`src/`, `app/`, `data/`) | `legacy/` | Replaced by `tests/` + `backend/`; pristine snapshot on `v1-legacy-baseline` branch |

---

## 3. Roadmap (bite-sized phases)

**Phase 0 — Foundation (½ day).** `pyproject.toml` + ruff/black/mypy/pytest, `pydantic-settings` config, `.github/workflows/ci.yml`, `docker-compose` (postgres+pgvector, redis). Green CI on an empty test.

**Phase 1 — Data layer.** SQLAlchemy 2.0 models (users, jobs, candidates, resumes, evaluations, audit_log), Alembic baseline (enable `vector` extension), repositories, one-shot importer for existing SQLite rows. *Exit:* `alembic upgrade head` on Postgres, repo unit tests pass.

**Phase 2 — Contracts & ports.** Convert `schemas.py` → Pydantic v2. Define `ports/` Protocols (`LLMProvider`, `Embedder`, `VectorStore`, `DocumentParser`). *Exit:* mypy clean.

**Phase 3 — FastAPI skeleton.** App factory, DI, health/readiness, RFC-7807 errors, jobs CRUD end-to-end. *Exit:* OpenAPI renders, integration test on `/jobs`.

**Phase 4 — Structured LLM + evaluation.** Anthropic adapter with `instructor`; multi-criteria rubric (Technical / Domain / Experience / Leadership) with CoT + gap analysis. Ollama adapter retained. *Exit:* validated `EvaluationResult`, snapshot test.

**Phase 5 — Parsing + hybrid retrieval.** Docling → structured JSON. Embed with bge-large; store vectors in pgvector. BM25 (reuse TF-IDF) + dense + **RRF** fusion. *Exit:* retrieval eval harness (recall@k) in `tests/evals`.

**Phase 6 — Async + resiliency.** Celery + Redis for `ingest_resume` / `batch_evaluate`. Tenacity retries, token-bucket limiter, circuit breaker around LLM calls. *Exit:* upload returns `202` + task id; status endpoint reports progress.

**Phase 7 — Observability.** OpenTelemetry on API + worker; LLM span attrs (model, tokens, cost, latency); Phoenix or LangSmith. *Exit:* one connected trace per ingest.

**Phase 8 — Frontend overhaul.** Streamlit as pure API client: NL search, candidate deep-dive (Plotly radar), side-by-side compare matrix, streaming Copilot, auto interview scorecard, dark-mode tokens.

**Phase 9 — MLOps hardening.** Ragas/DeepEval in CI as scoring/retrieval **drift gate**, full compose bring-up, coverage thresholds.

---

## 4. Core Code Skeletons

### `backend/core/schemas/evaluation.py`

```python
from enum import Enum
from pydantic import BaseModel, Field

class FitLevel(str, Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"

class RubricScore(BaseModel):
    criterion: str = Field(description="e.g. Technical Proficiency")
    score: float = Field(ge=0, le=10)
    reasoning: str = Field(description="Chain-of-thought justification, grounded in resume evidence")
    evidence: list[str] = Field(default_factory=list)

class GapAnalysis(BaseModel):
    missing_skills: list[str] = Field(default_factory=list)
    experience_gaps: list[str] = Field(default_factory=list)
    recommendation: str

class EvaluationResult(BaseModel):
    candidate_id: str
    job_id: str
    overall_score: float = Field(ge=0, le=100)
    fit_level: FitLevel
    rubric: list[RubricScore]                 # one per criterion
    strengths: list[str] = Field(default_factory=list)
    gaps: GapAnalysis
    summary: str
```

### `backend/core/ports/llm.py`

```python
from typing import Protocol, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class LLMProvider(Protocol):
    async def generate(self, prompt: str, system: str | None = None) -> str: ...
    async def structured(self, prompt: str, response_model: type[T],
                         system: str | None = None) -> T: ...
```

### `backend/adapters/llm/anthropic_provider.py`

```python
import instructor
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from backend.core.config import settings

class AnthropicProvider:
    def __init__(self) -> None:
        self._client = instructor.from_anthropic(
            AsyncAnthropic(api_key=settings.anthropic_api_key)
        )
        self._model = settings.llm_model  # e.g. "claude-sonnet-5"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=20))
    async def structured(self, prompt, response_model, system=None):
        return await self._client.messages.create(
            model=self._model, max_tokens=4096,
            system=system or "You are a helpful assistant.",
            messages=[{"role": "user", "content": prompt}],
            response_model=response_model,   # instructor validates → retries on schema failure
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=20))
    async def generate(self, prompt, system=None):
        msg = await self._client.messages.create(
            model=self._model, max_tokens=4096,
            system=system or "", messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
```

### `backend/services/evaluation_service.py`

```python
from backend.core.ports.llm import LLMProvider
from backend.core.schemas.evaluation import EvaluationResult

RUBRIC_CRITERIA = [
    "Technical Proficiency", "Domain Alignment",
    "Experience Depth", "Leadership Signal",
]

class EvaluationService:
    def __init__(self, llm: LLMProvider) -> None:
        self._llm = llm

    async def evaluate(self, candidate: dict, job: dict) -> EvaluationResult:
        system = (
            "You are an expert technical recruiter. Score the candidate against "
            "each rubric criterion. Think step by step before assigning each score, "
            "and cite specific resume evidence. Do not invent facts."
        )
        prompt = self._build_prompt(candidate, job, RUBRIC_CRITERIA)
        return await self._llm.structured(
            prompt=prompt, system=system, response_model=EvaluationResult,
        )

    def _build_prompt(self, candidate, job, criteria) -> str:
        return (
            f"JOB:\n{job}\n\nCANDIDATE:\n{candidate}\n\n"
            f"Evaluate against: {', '.join(criteria)}."
        )
```

### `backend/services/retrieval_service.py`

```python
from backend.core.ports.vector_store import VectorStore
from backend.core.ports.embedder import Embedder

class RetrievalService:
    def __init__(self, vectors: VectorStore, embedder: Embedder, bm25) -> None:
        self._vectors, self._embedder, self._bm25 = vectors, embedder, bm25

    async def search(self, query: str, k: int = 20, rrf_k: int = 60) -> list[str]:
        dense = await self._vectors.query(await self._embedder.embed(query), top_k=k)
        sparse = self._bm25.query(query, top_k=k)   # reuse existing TF-IDF/BM25 logic
        return self._reciprocal_rank_fusion([dense, sparse], k=rrf_k)[:k]

    @staticmethod
    def _reciprocal_rank_fusion(rankings: list[list[str]], k: int) -> list[str]:
        scores: dict[str, float] = {}
        for ranking in rankings:
            for rank, doc_id in enumerate(ranking):
                scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
        return sorted(scores, key=scores.get, reverse=True)
```

### `backend/api/v1/resumes.py` (async ingestion)

```python
from fastapi import APIRouter, UploadFile, status
from backend.workers.tasks import ingest_resume

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def upload_resume(file: UploadFile):
    raw = await file.read()
    task = ingest_resume.delay(file.filename, raw)   # parse → embed → index → persist
    return {"task_id": task.id, "status": "queued"}
```

---

## 5. Key Decisions & Rationale

1. **Instructor over BAML** — smallest jump from the current `LLMClient`; Pydantic-validated JSON with auto retry-on-schema-failure. Directly fixes the `json.loads(response)` fragility.
2. **pgvector over Qdrant** — Postgres is already in the stack, so this is *less* infra (no extra container). Good to ~1M vectors. Baseline Alembic migration must `CREATE EXTENSION vector;`.
3. **Keep the Ollama path** — the `LLMProvider` port lets Claude (prod) and Ollama (local/offline demo) coexist. Strong interview talking point.
4. **Archive, don't delete, the 70 `test_day*.py` files** — evidence of the build journey, but excluded from CI.

---

## 6. Open Follow-ups

- Auth model (JWT vs. session) for the user-management tables — deferred to Phase 1 detail.
- Embedding model host: local `bge-large-en-v1.5` (no cost, needs GPU/CPU budget) vs. hosted (Voyage) — decide at Phase 5.
- Whether Copilot streaming uses SSE (simpler) or WebSocket (bidirectional) — SSE recommended.
