# Interview Prep — AI Resume Intelligence & Interview Copilot

Your complete study guide for talking about this project in placement interviews.
**Goal: understand it, don't memorize it.** Interviewers probe follow-ups; if you
understand *why* each choice was made, you can answer anything. Every section below
explains the concept first, then how it's used here.

> Honesty rule for interviews: know the parts you'd improve (there's a "Limitations"
> section). Admitting a tradeoff you understand impresses more than pretending it's perfect.

## Table of contents
1. [30-second / 2-minute pitch](#1-the-pitch)
2. [What problem it solves](#2-the-problem)
3. [Architecture (the big idea)](#3-architecture)
4. [Tech stack — what and why](#4-tech-stack--what-and-why)
5. [Core concepts you MUST understand](#5-core-concepts-you-must-understand)
6. [How each feature works (end to end)](#6-how-each-feature-works)
7. [Key engineering decisions & tradeoffs](#7-key-engineering-decisions--tradeoffs)
8. [Q&A bank](#8-qa-bank)
9. [System-design discussion / whiteboard](#9-system-design-discussion)
10. [Limitations & "what would you improve"](#10-limitations--what-i-would-improve)
11. [STAR stories](#11-star-stories)
12. [Numbers & facts to remember](#12-numbers--facts-to-remember)
13. [What to learn (study roadmap)](#13-what-to-learn--study-roadmap)

---

## 1. The pitch

**30-second version:**
> "I built an enterprise-grade AI recruiting platform. Recruiters upload resumes, and
> the system parses them, stores them in a vector database, and lets you search
> candidates by meaning — not just keywords — using hybrid search. It scores each
> candidate against a job with an LLM that returns a structured rubric, and there's a
> streaming AI copilot to ask questions about candidates. It's a FastAPI backend with a
> clean domain-driven architecture, async workers, and it works with multiple LLM
> providers — Claude, Gemini, or a local model — just by changing config."

**2-minute version** adds: the architecture (ports & adapters, so any LLM/DB/parser is
swappable), the reliability layer (retries, rate limiting, circuit breaker), production
concerns (async task queue, observability, CI, evaluation gates), and that it's verified
end-to-end against a real managed Postgres and a live LLM.

**One-liner:** "A production-shaped RAG + structured-LLM system for recruiting, built
with clean architecture and swappable providers."

---

## 2. The problem

Traditional resume screening is either **manual** (slow, subjective) or **keyword-based**
(an ATS that misses a "great fit" because they wrote "NLP" instead of "natural language
processing"). This platform solves three things:

1. **Semantic matching** — find candidates by *meaning* (embeddings), so "built
   transformers" matches a search for "NLP experience."
2. **Explainable scoring** — an LLM scores each candidate on a rubric with reasoning and
   evidence, not an opaque number.
3. **Speed at scale** — async ingestion and bulk evaluation so a recruiter can process
   hundreds of resumes without blocking.

---

## 3. Architecture

### The big idea: Ports & Adapters (Hexagonal / Clean Architecture, DDD-flavored)

The core business logic depends on **abstractions (ports)**, never on concrete tools.
Concrete tools (**adapters**) plug in at the edges. Result: you can swap the LLM
(Claude → Gemini → Ollama), the vector store, or the parser **without touching business
logic** — it's a config change.

```
API layer (FastAPI)        ← HTTP, validation, dependency injection
      │
Services (use-cases)       ← "ingest a resume", "evaluate a candidate", "search"
      │  depends on ↓ (abstract)
Ports (Protocols)          ← LLMProvider, Embedder, VectorStore, DocumentParser
      ▲  implemented by
Adapters (concrete)        ← AnthropicProvider, GeminiProvider, FastEmbedEmbedder,
                             PgVectorStore, PyMuPDFParser, Bm25Retriever
      │
Infrastructure             ← Postgres+pgvector, Redis, LLM APIs
```

**Why this matters (say this in the interview):** "When the user only had a Gemini key
instead of Claude, adding Gemini was one new adapter file implementing the same
`LLMProvider` interface — extraction, evaluation, and the copilot all worked unchanged.
That's the whole point of the abstraction, and I proved it end to end."

### Layer responsibilities
- **`core/ports`** — Python `Protocol` classes defining interfaces (structural typing).
- **`core/schemas`** — Pydantic models: API request/response + LLM structured-output contracts.
- **`services`** — orchestration/use-cases; pure-ish, testable with fakes.
- **`adapters`** — vendor-specific implementations.
- **`api/v1`** — FastAPI routers, dependency injection, error handling.
- **`db`** — SQLAlchemy models, repositories, Alembic migrations.
- **`workers`** — Celery tasks for heavy async work.

---

## 4. Tech stack — what and why

| Tech | What it is | Why chosen (say this) |
|---|---|---|
| **FastAPI** | Async Python web framework | Native async (good for I/O-bound LLM calls), automatic OpenAPI docs, Pydantic validation built in |
| **Pydantic v2** | Data validation via type hints | Validates API I/O *and* enforces LLM JSON structure; v2 is Rust-backed and fast |
| **SQLAlchemy 2.0 (async)** | ORM | Type-safe models, async engine to match FastAPI; repositories keep DB code isolated |
| **Alembic** | DB migrations | Versioned, reviewable schema changes; the baseline enables the pgvector extension |
| **PostgreSQL + pgvector** | Relational DB + vector search | One database for both relational data and embeddings → less infra than a separate vector DB |
| **fastembed** | ONNX embedding models | CPU-friendly, **no PyTorch** — runs on a laptop with no GPU; picked `bge-base-en-v1.5` (768-dim) |
| **rank-bm25** | Keyword (lexical) ranking | The sparse half of hybrid search |
| **Celery + Redis** | Distributed task queue | Offload slow PDF parsing/embedding/eval so the API returns instantly (202 + task id) |
| **Instructor** | Structured LLM output | Forces Claude to return schema-valid JSON, with auto-retry — replaced fragile `json.loads` |
| **google-genai** | Gemini SDK | Native `response_schema` for structured output |
| **Tenacity** | Retry library | Exponential backoff on transient LLM/API failures |
| **OpenTelemetry** | Observability/tracing | Traces latency, token usage, and cost per LLM call |
| **Streamlit + Plotly** | Frontend | Fast to build data UIs; Plotly for the competency radar charts |
| **PyMuPDF** | PDF parsing | Fast, pure-CPU text extraction (vs. heavier ML parsers like Docling) |
| **ruff / black / mypy / pytest** | Quality tooling | Lint / format / strict type-check / test — enforced in CI |

---

## 5. Core concepts you MUST understand

These are the highest-probability deep-dive topics. Understand each well enough to draw it.

### 5.1 Embeddings & vector search
- An **embedding** is a list of numbers (a vector, here 768-dim) representing the *meaning*
  of text. Similar meanings → vectors close together.
- **Similarity** is measured by **cosine similarity** (angle between vectors). pgvector's
  `<=>` operator gives cosine *distance*; similarity = `1 - distance`.
- **Vector search** = "find the stored vectors nearest to the query vector."
- **ANN index (HNSW)**: exact nearest-neighbour is O(n); at scale you use an approximate
  index (Hierarchical Navigable Small World graph) for fast sub-linear search. *We note
  this as a production add-on.*

### 5.2 Hybrid search + Reciprocal Rank Fusion (RRF) — **flagship topic**
- **Dense (semantic)** search finds meaning but can miss exact terms (e.g. a specific
  library name). **Sparse (BM25 keyword)** nails exact terms but misses synonyms.
- **Hybrid** runs both and **fuses** the rankings. We use **RRF**: each document gets
  `score = Σ 1/(k + rank_in_that_list)` across the two rankings (k≈60). Documents ranked
  highly by *both* bubble to the top.
- **Why RRF over combining raw scores?** Dense cosine scores and BM25 scores are on
  different scales; you can't just add them. RRF only uses *rank position*, so it's
  scale-independent — no normalization needed. **This is a great thing to explain.**

```
RRF(d) = Σ  1 / (k + rank_i(d))     # sum over each ranker i; k dampens top-rank dominance
```

### 5.3 RAG (Retrieval-Augmented Generation)
- Instead of asking an LLM from memory, you **retrieve** relevant context first, then put
  it in the prompt so the model answers grounded in real data.
- Here: the copilot retrieves candidate context and answers only from it (reduces
  hallucination). The evaluator is fed the actual resume + job.

### 5.4 Structured LLM output
- LLMs return text; apps need reliable JSON. **Instructor** (Claude) and Gemini's
  **`response_schema`** make the model return data validated against a **Pydantic** model,
  retrying if it doesn't conform. This is the difference between "usually works" and
  "production-safe."
- **Chain-of-thought**: we ask the model to reason step-by-step before scoring, which
  improves quality and gives explainability (the `reasoning` field per rubric criterion).

### 5.5 Async / concurrency (Python)
- **`async`/`await`** lets one thread handle many I/O-bound operations (network/LLM/DB
  calls) by not blocking while waiting. Perfect for an API that mostly waits on external
  services.
- **Event loop**: the scheduler that runs coroutines. (War story: on Windows, async
  `psycopg` needs the *Selector* event loop, not the default *Proactor* — a real bug I fixed.)
- **Concurrency vs parallelism**: async = concurrency (interleaving I/O waits, one core);
  Celery workers = parallelism (multiple processes). We use async for the API and Celery
  for CPU-heavy background work.

### 5.6 Task queues (Celery + Redis)
- The API shouldn't block for 10s parsing+embedding a PDF. It pushes a **task** to a
  **queue (Redis)** and returns `202 Accepted` + a task id. A **worker** process picks it
  up. The client polls a status endpoint. This is the **producer/consumer** pattern.

### 5.7 Resilience patterns (around external LLM calls)
- **Retry with exponential backoff** (Tenacity): transient failures (429/503) are retried
  with growing delays.
- **Rate limiter (token bucket)**: caps request rate to respect provider quotas. Tokens
  refill at a fixed rate; each call spends one; if empty, wait.
- **Circuit breaker**: if a dependency keeps failing, "open the circuit" and fail fast for
  a cooldown instead of hammering a dead service. States: **closed** (normal) → **open**
  (fail fast) → **half-open** (test one call) → closed/open again.

### 5.8 Dependency Injection (DI)
- FastAPI's `Depends` supplies things (DB session, services) to endpoints. Benefits:
  endpoints don't construct their own dependencies (loose coupling), and tests can
  **override** them with fakes. We use this heavily to test endpoints without a real DB/LLM.

---

## 6. How each feature works

### Resume ingestion (async)
`POST /resumes` → reads bytes, base64-encodes, enqueues a Celery task, returns `202` +
task id. Worker: **parse** (PyMuPDF) → **extract identity/attributes** (LLM structured
output, with a regex/heuristic fallback if no LLM or it fails) → **upsert candidate**
(by email) → **embed** the text (fastembed) → **persist** the resume with its vector.

### Hybrid search
`POST /search` → embed the query → **dense** kNN via pgvector cosine + **sparse** BM25 →
**RRF fusion** → ranked candidate ids.

### Evaluation (single + batch)
`POST /evaluations` → load candidate + job → LLM returns a validated `EvaluationResult`
(overall score, fit level, per-criterion rubric with reasoning + evidence, gap analysis).
`POST /evaluations/batch` evaluates many candidates concurrently (bounded semaphore),
upserts results, and **tolerates per-candidate failures** (partial results).

### Copilot (streaming)
`POST /copilot/stream` → gather candidate context → LLM **streams** tokens back as
**Server-Sent Events** (`text/event-stream`, `data: {...}` frames). The frontend renders
them live. Mid-stream errors are sent as an in-band error event (connection isn't dropped).

### Observability
Every LLM call opens an OpenTelemetry **span** with model, input/output tokens, estimated
cost, and latency (`gen_ai.*` attributes) — exportable to Phoenix/any OTLP collector.

---

## 7. Key engineering decisions & tradeoffs

Interviewers love "why did you choose X over Y." These are real decisions from the build:

| Decision | Alternative | Why |
|---|---|---|
| **pgvector** | Dedicated vector DB (Qdrant/Pinecone) | Already using Postgres → one less service. Fine to ~1M vectors. Would switch to a dedicated DB at larger scale. |
| **fastembed (ONNX)** | sentence-transformers (PyTorch) | Target machine had **no GPU**; fastembed runs fast on CPU without the 2GB torch dependency. |
| **PyMuPDF** | Docling / Unstructured | Those load ML models (slow, RAM-heavy on CPU). PyMuPDF is fast/pure-CPU; the parser is behind a port so Docling can slot in later. |
| **Instructor / response_schema** | `json.loads(llm_output)` | Guaranteed schema-valid output with auto-retry vs. fragile parsing that breaks when the model adds prose. |
| **RRF fusion** | Weighted sum of scores | Scale-independent (no need to normalize dense vs BM25 scores). |
| **Ports & adapters** | Direct calls to Claude SDK everywhere | Provider swap = one file. Proven when we added Gemini. |
| **Sync batch endpoint + Celery task** | Only Celery | The dev network blocked Redis's port; a sync path meant bulk eval still worked. Both share one service. |
| **Separate frontend venv** | One venv | Streamlit's deps conflicted with backend deps in the resolver; isolation mirrors how they deploy (separate containers). |

---

## 8. Q&A bank

### General / behavioral
**Q: Walk me through your project.** → Use the 2-minute pitch, then offer to go deep on
any layer.

**Q: What was the hardest part?** → "Making LLM output reliable. Models return text;
production needs guaranteed structure. I moved from parsing raw JSON to schema-enforced
structured outputs with auto-retry, plus a resilience layer (retries, rate limiter,
circuit breaker) because external LLM APIs fail and throttle. During live testing on
Gemini's free tier I hit 503/429 spikes, which exposed two robustness gaps — batch failing
wholesale and streaming dropping the connection — so I made batch return partial results
and streaming emit in-band error events."

**Q: What would you do differently / improve?** → See [section 10].

**Q: Is this your own work?** → Be honest and specific about *understanding*: "I designed
the architecture and made the engineering decisions; I can explain any part and the
tradeoffs." Then demonstrate by going deep on something.

### System design / architecture
**Q: Why ports & adapters?** → Decoupling + testability + swappable vendors. Concrete
proof: added Gemini as one adapter; tests use fake adapters so they need no DB/LLM.

**Q: How do you test code that calls an LLM/DB?** → Dependency injection + fakes. Endpoints
depend on abstractions; tests override them with fake providers returning canned data. DB
tests use an in-memory SQLite for portable tables and are skipped/gated for pgvector-only
features (`RUN_DB_TESTS=1` runs them against real Postgres).

**Q: How would this scale to millions of resumes?** → See [section 9].

**Q: How do you handle a slow 10-second operation in an API?** → Don't block. Enqueue to
Celery, return 202 + task id, poll for status (or webhook). Producer/consumer via Redis.

### Retrieval / AI
**Q: Explain hybrid search and RRF.** → [Section 5.2]. Emphasize scale-independence of RRF.

**Q: What's an embedding? How do you compare them?** → [Section 5.1]. Cosine similarity.

**Q: Dense vs sparse retrieval — when does each win?** → Dense: synonyms/meaning
("ML" ↔ "machine learning"). Sparse/BM25: exact terms, rare tokens, names. Hybrid gets both.

**Q: How do you stop the LLM from hallucinating?** → RAG (ground answers in retrieved
context), structured outputs (constrain format), chain-of-thought + evidence fields,
and an explicit "don't invent facts" instruction. Plus an eval gate to catch drift.

**Q: How do you know your retrieval/scoring is good (evaluation)?** → IR metrics —
recall@k, MRR, nDCG — over a labeled "golden" set, run as a CI gate that fails if quality
drops below a threshold (retrieval drift). Scoring is checked by asserting a strong
candidate outscores a weak one.

**Q: What is pgvector and how does it search?** → A Postgres extension adding a `vector`
column type and distance operators (`<=>` cosine). `ORDER BY embedding <=> query LIMIT k`
returns nearest neighbours; add an HNSW index for speed at scale.

### Python / backend
**Q: async vs threads vs processes?** → async = single-thread cooperative concurrency for
I/O-bound; threads limited by the GIL for CPU work; processes (Celery) for true
parallelism/CPU-bound. We use async for the API, processes for background CPU work.

**Q: What's Pydantic doing for you?** → Runtime validation from type hints for API I/O and
LLM output; clear errors; serialization. v2 is much faster (Rust core).

**Q: Repository pattern — why?** → Isolates DB access behind a class so services don't
write raw queries; swappable and testable.

**Q: How do migrations work?** → Alembic versions schema changes as reviewable scripts;
`upgrade head` applies them; the baseline also enables the pgvector extension.

### DevOps / production
**Q: How is it deployed?** → Dockerized (multi-stage: api/worker/frontend), docker-compose
with a one-shot migration job, or managed Postgres/Redis + a container host. CI runs
lint/format/type/test on every push.

**Q: How do you handle secrets?** → Env vars / `.env` (gitignored), never committed;
a secret manager in real prod.

**Q: What's your CI doing?** → ruff (lint), black (format check), mypy --strict (types),
pytest (tests + eval gates).

---

## 9. System-design discussion

If asked to "design/scale this," talk through:

**Scaling reads (search):** add an HNSW index on the vector column; cache hot queries;
read replicas for Postgres. Move BM25 from in-memory to Postgres full-text or a dedicated
search engine (OpenSearch) so it's not rebuilt per request (a known current limitation).

**Scaling ingestion:** more Celery workers (scale on queue depth); batch-embed; stream
large files; store raw files in object storage (S3), not the DB.

**Scaling evaluation (LLM):** the bottleneck is the provider's rate limit and cost, not
your code. Use batching, caching of identical requests, a cheaper model for bulk, bounded
concurrency, and the circuit breaker to fail fast during outages.

**Reliability:** retries + circuit breaker (have it), health/readiness probes (have),
graceful degradation (have — partial batches, in-band stream errors), idempotent ingestion
(upsert by email — have).

**Data model:** users, jobs, candidates, resumes (with `vector` embedding), evaluations
(unique per candidate+job), audit_log. Relational for integrity + vectors in the same DB.

**Multi-tenancy (if asked):** add an org/tenant id to every table + row-level scoping.

**Cost control:** track tokens/cost per call (OpenTelemetry), pick model per task, cache,
lower "effort" for simple tasks.

---

## 10. Limitations & "what I would improve"

Knowing these makes you look senior. Volunteer one or two.

- **BM25 is rebuilt in memory per search request** — fine for a demo, won't scale. Fix:
  Postgres full-text index or OpenSearch.
- **No vector ANN index yet** — exact search is O(n); add HNSW before large pools.
- **No authentication/authorization** — the `users` table exists but there's no JWT/login
  flow yet. Would add OAuth2/JWT + role-based access.
- **Raw files stored as text in the DB** — should use object storage (S3) with a reference.
- **The Celery async hop wasn't tested on the dev machine** (ISP blocked Redis's port 6379);
  the sync paths were verified. Would confirm on unrestricted infra.
- **Name/attribute extraction quality** depends on the LLM; heuristic fallback is basic.
- **No reranker** — a cross-encoder reranking stage after retrieval would boost precision.
- **Cost/latency of LLM eval** — bulk scoring is provider-rate-limited; a fine-tuned smaller
  model or caching would help.

---

## 11. STAR stories

Use **Situation-Task-Action-Result** for behavioral questions.

**Reliability under a flaky dependency:**
- *S:* Testing evaluation on a live LLM free tier, requests intermittently returned 503/429.
- *T:* The batch endpoint failed entirely and the streaming endpoint dropped the connection.
- *A:* Made batch use `gather(return_exceptions=True)` for partial results, and wrapped the
  SSE generator to emit an in-band error event + `[DONE]` instead of crashing. Added tests
  with fake providers that raise mid-stream.
- *R:* Batch now returns 201 with whatever succeeded; the stream ends cleanly. Verified live.

**Extensibility paying off:**
- *S:* The plan targeted Claude, but only a Gemini key was available.
- *T:* Support Gemini without rewriting features.
- *A:* Implemented one `GeminiProvider` against the existing `LLMProvider` port (native
  `response_schema` for structured output) and a factory + config switch.
- *R:* Extraction, evaluation, batch, and streaming all worked on Gemini unchanged —
  proof the abstraction was worth it.

**Debugging a platform-specific bug:**
- *S:* API calls to Postgres failed only when run through the server on Windows.
- *T:* Find why async DB worked in scripts but not under uvicorn.
- *A:* Diagnosed that uvicorn forces Windows' Proactor event loop, which async psycopg
  can't use; ran the server under a Selector-loop entrypoint (`python -m backend`).
- *R:* API works on Windows; documented the caveat.

---

## 12. Numbers & facts to remember

- Embeddings: **768-dim** (`bge-base-en-v1.5` via fastembed/ONNX).
- RRF constant **k ≈ 60**; score = Σ 1/(k + rank).
- Circuit breaker: opens after **5** failures, ~**30s** cooldown (configurable).
- Async upload returns **202 Accepted** + task id.
- Rubric criteria: **Technical Proficiency, Domain Alignment, Experience Depth, Leadership Signal**.
- Providers: **Anthropic (Claude), Gemini, Ollama** — switch via `LLM_PROVIDER`.
- Errors follow **RFC 7807** (`application/problem+json`).
- Tables: users, jobs, candidates, resumes, evaluations, audit_log.
- Quality gate: **ruff, black, mypy --strict, pytest** in CI.

---

## 13. What to learn — study roadmap

Prioritized. Focus on the **must-know** tier first; that's what gets asked.

### Tier 1 — must know cold (the project's spine)
- **Python**: functions/classes, type hints, `async`/`await`, list/dict comprehensions,
  decorators, context managers, exceptions.
- **REST APIs & HTTP**: methods, status codes (200/201/202/400/404/422/500/503), JSON,
  request/response lifecycle.
- **FastAPI**: path/query/body params, Pydantic models, dependency injection, async endpoints.
- **Databases/SQL**: tables, keys, joins, indexes, transactions; ORM basics; what a
  migration is.
- **Embeddings + vector search + cosine similarity** (section 5.1).
- **Hybrid search + RRF** (section 5.2) — your differentiator; be able to explain and draw it.
- **RAG + structured outputs** (5.3, 5.4).

### Tier 2 — strongly expected
- **Async concurrency** vs threads vs processes; the event loop; the GIL.
- **Task queues** (Celery/Redis) and the producer/consumer pattern.
- **Resilience patterns**: retry/backoff, rate limiting (token bucket), circuit breaker.
- **Clean/Hexagonal architecture, SOLID, dependency inversion** — the "why" behind ports/adapters.
- **Testing**: unit vs integration, mocking/fakes, why DI helps testing.
- **Docker** basics: image vs container, Dockerfile, docker-compose, multi-stage builds.
- **Git**: branches, PRs, merge; you did the full flow.

### Tier 3 — bonus (sets you apart)
- **Observability**: tracing/metrics/logs; what OpenTelemetry does.
- **Vector DB internals**: ANN, HNSW, when to use a dedicated vector DB.
- **LLM concepts**: tokens, context window, temperature, prompt engineering, hallucination,
  evaluation (recall@k, MRR, nDCG), rerankers.
- **CI/CD** and code-quality tooling (linters, formatters, type checkers).
- **12-factor app** principles (config in env, stateless processes, etc.).

### How to study (2-week plan)
1. **Days 1-3:** Re-read the codebase top-down: `core/ports` → `services` → `adapters` →
   `api/v1`. For each file, say out loud what it does and why.
2. **Days 4-6:** Run it locally. Ingest a resume, search, evaluate, chat. Watch the data
   flow. Break something on purpose and read the error.
3. **Days 7-9:** Master Tier-1 concepts; practice explaining hybrid search + RRF on paper.
4. **Days 10-12:** Do a mock: give the 2-min pitch, then answer 10 random questions from
   section 8 without looking.
5. **Days 13-14:** Learn the Tier-2 "why"s; prepare your STAR stories; skim Tier 3.

### Free resources
- FastAPI docs (excellent tutorial) · SQLAlchemy 2.0 async docs · pgvector README ·
  "The Twelve-Factor App" · Martin Fowler on Circuit Breaker & Hexagonal Architecture ·
  any "RAG explained" and "reciprocal rank fusion" article · Python `asyncio` docs.

---

### Final tips
- **Lead with the architecture and the provider-swap story** — it's your strongest, most
  memorable point.
- **Draw the hybrid-search diagram** when retrieval comes up.
- **Volunteer a limitation + fix** — it signals maturity.
- If you don't know something, say "I haven't used that, but based on X I'd approach it
  like…" — reasoning beats bluffing.
