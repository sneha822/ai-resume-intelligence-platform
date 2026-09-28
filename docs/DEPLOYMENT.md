# Deployment Guide

How to run the AI Resume Intelligence platform in production. It has four
long-running pieces — **API**, **worker**, **frontend** — plus two stateful
dependencies: **Postgres (with pgvector)** and **Redis**.

```
              ┌─────────────┐
  users ────▶ │  frontend   │ ──HTTP──▶ ┌──────────┐ ──▶ Postgres + pgvector
  (browser)   │ (Streamlit) │           │   API    │ ──▶ Redis ──▶ ┌────────┐
              └─────────────┘           │ (FastAPI)│               │ worker │ ──▶ same DB
                                        └──────────┘               │(Celery)│
                                             │                     └────────┘
                                             └──▶ LLM provider (Anthropic / Gemini / Ollama)
```

Pick one of three paths below. All of them share the same **prerequisites** and
**post-deploy verification**.

---

## Prerequisites

- **Container runtime** (Docker + Compose) for the container paths.
- **Postgres 16+ with the `pgvector` extension.** The baseline migration runs
  `CREATE EXTENSION vector`, so the DB role needs permission to create extensions
  (managed pgvector providers like Neon allow this).
- **Redis** for Celery broker/result backend.
- **An LLM provider key** — one of `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`
  (or `GOOGLE_API_KEY`), or a reachable **Ollama** host. Without one, LLM
  endpoints return `503`; ingestion/search/CRUD still work.
- **Secrets** supplied via environment / secret manager — never commit `.env`.

### Required environment variables

| Variable | Notes |
|---|---|
| `DATABASE_URL` | `postgresql+psycopg://user:pass@host:5432/db` (async driver). Managed Neon: append `?sslmode=require&channel_binding=disable`. |
| `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` | Redis. Managed Upstash: `rediss://…?ssl_cert_reqs=required`; free tier is single-DB, use `/0`. |
| `LLM_PROVIDER` | `anthropic` \| `gemini` \| `ollama` |
| `ANTHROPIC_API_KEY` + `LLM_MODEL` | e.g. `claude-sonnet-5` |
| `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) + `GEMINI_MODEL` | e.g. `gemini-3.8-flash` |
| `EMBEDDING_MODEL`, `EMBEDDING_DIM` | Default `BAAI/bge-base-en-v1.5` / `768`. **If you change the model, the dim must match the `resumes.embedding` column** (see "Changing the embedding model"). |
| `DEBUG` | Set `false` in production (disables SQL echo). |
| `OTEL_ENABLED`, `OTEL_EXPORTER_OTLP_ENDPOINT` | Optional tracing → Phoenix/any OTLP collector. |

---

## Path A — Single host with Docker Compose (recommended to start)

Runs everything (DB, Redis, API, worker, frontend) on one VM. Good for demos,
staging, and small production.

```bash
# 1. Clone + configure
git clone <repo> && cd ai-resume-intelligence-platform
cp .env.example .env      # fill in secrets; set DEBUG=false and an LLM key

# 2. Build + start (prod overrides: runs migrations, no --reload, restart policies)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# 3. Watch it come up
docker compose logs -f migrate   # should exit 0 after "Running upgrade -> 0001_baseline"
docker compose ps
```

The prod override adds a one-shot **`migrate`** service (runs `alembic upgrade head`
and must complete before API/worker start) and a **`frontend`** service on `:8501`.

Put a TLS-terminating reverse proxy (Caddy, nginx, or Traefik) in front of the API
(`:8000`) and frontend (`:8501`). Don't expose Postgres/Redis publicly.

---

> **One-click option:** this repo ships a **Render Blueprint** (`render.yaml`). See
> **[docs/deploy-render.md](deploy-render.md)** to deploy API + worker + frontend from
> GitHub with your Neon + Upstash data — no local Docker needed.

## Path B — Managed data + container host (recommended for real production)

Offload state to managed services (no DB/Redis ops), run the app containers on a
PaaS or VM. This is what was used to verify the platform end-to-end (Neon + Upstash).

1. **Postgres**: create a managed pgvector Postgres (e.g. Neon). Copy its
   connection string into `DATABASE_URL` as `postgresql+psycopg://…?sslmode=require&channel_binding=disable`.
2. **Redis**: create a managed Redis (e.g. Upstash). Use the `rediss://` TLS URL with
   `?ssl_cert_reqs=required` for `REDIS_URL` / `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND`.
3. **Migrate once** (from CI, a shell, or the `migrate` container):
   ```bash
   DATABASE_URL=... python -m alembic upgrade head
   ```
4. **Deploy the images.** Build the three targets and run them on your host/PaaS
   (Render, Railway, Fly.io, ECS, Cloud Run, a plain VM…):
   - API — image target `api`, command `uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers <N>`
   - Worker — image target `worker`, command `celery -A backend.workers.celery_app worker --concurrency <N>`
   - Frontend — image target `frontend` (set `AIRI_API_URL` to the public API URL)

   With managed data, delete the `postgres`/`redis` services from the compose files,
   or run the containers directly:
   ```bash
   docker build --target api      -t airi-api .
   docker build --target worker   -t airi-worker .
   docker build --target frontend -t airi-frontend .
   ```

---

## Path C — Kubernetes (sketch)

For scale, map each piece to a workload:

| Component | Workload | Notes |
|---|---|---|
| API | `Deployment` + `Service` + HPA | `readinessProbe: GET /ready`, `livenessProbe: GET /health` |
| Worker | `Deployment` (HPA on queue depth) | no probes; scale on Redis backlog |
| Frontend | `Deployment` + `Service` | env `AIRI_API_URL` = in-cluster API service |
| Migrations | `Job` (or Helm pre-install/pre-upgrade hook) | `python -m alembic upgrade head`, run to completion before rollout |
| Postgres / Redis | managed services or operators | pgvector required |

Store secrets in a `Secret`, mount as env. Point `OTEL_EXPORTER_OTLP_ENDPOINT` at
your collector.

---

## Post-deploy verification

```bash
API=https://your-api.example.com

curl -s $API/health          # {"status":"healthy",...}
curl -s $API/ready           # {"status":"ready"}

# Create a job
curl -s -X POST $API/api/v1/jobs -H 'content-type: application/json' \
  -d '{"title":"ML Engineer","description":"RAG, NLP, Python"}'

# Upload a resume (async → returns a task id)
curl -s -X POST $API/api/v1/resumes -F 'file=@resume.pdf'
# → {"task_id":"...","status":"queued"}   (worker + Redis must be running)

# Hybrid search
curl -s -X POST $API/api/v1/search -H 'content-type: application/json' \
  -d '{"query":"nlp engineer","top_k":5}'
```

Then open the frontend and confirm the dashboard shows healthy API + candidate/job counts.

---

## Operational notes

### Scaling
- **API**: stateless — scale horizontally (`--workers` per container, and/or more
  replicas behind the proxy).
- **Worker**: scale on Redis queue depth; set `--concurrency` to balance CPU
  (embedding is CPU-bound) against your LLM provider's rate limits.
- **Embeddings**: fastembed downloads the ONNX model on first use. Warm it at
  startup (or bake it into the image) so the first request isn't slow; the model is
  cached on disk per container — use a volume to persist it across restarts.

### pgvector index (do this before large pools)
The baseline creates the `vector` column but no ANN index. For datasets beyond a
few thousand resumes, add an HNSW index so nearest-neighbour search stays fast
(create it in a new Alembic migration):
```sql
CREATE INDEX ON resumes USING hnsw (embedding vector_cosine_ops);
```

### Changing the embedding model
`EMBEDDING_DIM` must equal the `resumes.embedding` vector dimension. To switch
models, write a migration that alters the column to the new dimension and re-embed
existing resumes (re-ingest), then update `EMBEDDING_MODEL`/`EMBEDDING_DIM`.

### LLM providers & cost
- Provider is chosen by `LLM_PROVIDER`; the resilient wrapper adds retries + a
  rate limiter + a circuit breaker. Tune `TokenBucketRateLimiter` to your quota.
- Batch evaluation and streaming degrade gracefully under provider `429`/`503`
  (partial batches; in-band SSE error events).
- Watch spend/latency via the OpenTelemetry `gen_ai.*` span attributes.

### Windows note
Only relevant if you run the app processes natively on Windows (not in containers):
launch the API with `python -m backend` (sets the SelectorEventLoop for async
psycopg) and the worker with `--pool=solo`. Linux containers need neither.

### Security checklist
- [ ] `DEBUG=false`; secrets from a manager, never committed
- [ ] TLS at the proxy; API/frontend not served plaintext
- [ ] Postgres/Redis not publicly reachable; strong credentials; TLS to managed data
- [ ] Rotate any keys that were shared during setup
- [ ] Restrict CORS/origins at the proxy as needed
- [ ] Back up Postgres (managed snapshots or `pg_dump`)

---

## Rollback

- **App**: redeploy the previous image tag.
- **Schema**: `python -m alembic downgrade -1` (the baseline `downgrade()` drops the
  schema + extension — review before running against data you care about).
