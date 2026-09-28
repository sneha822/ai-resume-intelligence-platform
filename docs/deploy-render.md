# Deploy to Render (free) — step by step

Deploys the **API + Streamlit frontend** from your GitHub repo using the `render.yaml`
Blueprint. Data stays on **Neon** (Postgres+pgvector). Ingestion runs **synchronously**
(`INGEST_MODE=sync`) so **no Celery worker and no Redis are needed** — both services run
on Render's **free** plan. Total cost: **$0**.

> Free web services sleep after ~15 min idle and cold-start (~30–60s) on the next
> request. Fine for a portfolio/demo link. (Want the async worker instead? See the
> commented block at the bottom of `render.yaml`.)

## Prerequisites
- Neon `DATABASE_URL` and a `GEMINI_API_KEY` (both already in your local `.env`).
- Repo on GitHub (it is).

## Steps

### 1. Sign up
<https://render.com> → **Sign up with GitHub**, authorize your repos.

### 2. Create the Blueprint
Dashboard → **New +** → **Blueprint** → pick `sneha822/ai-resume-intelligence-platform`,
branch `main` → **Apply**. Render reads `render.yaml` and shows `airi-api` + `airi-frontend`
+ the `airi-secrets` group.

### 3. Fill in the secrets (prompted for `sync: false` values)
| Key | Value (copy from your local `.env`) |
|---|---|
| `DATABASE_URL` | `postgresql+psycopg://…@…neon.tech/…?sslmode=require&channel_binding=disable` |
| `GEMINI_API_KEY` | your Gemini key |

(`LLM_PROVIDER=gemini`, `GEMINI_MODEL`, `EMBEDDING_*`, and `INGEST_MODE=sync` are already
set in the Blueprint.)

### 4. First deploy
Apply. Watch the **`airi-api`** logs — on boot it runs `alembic upgrade head` (creates the
tables + pgvector extension on Neon) then starts uvicorn. Wait for healthy.

### 5. Seed demo data (so the live app looks full)
Run once against the **same Neon DB** (from your machine, `.env` pointed at Neon):
```bash
.venv/Scripts/python -m backend.db.seed
```
This adds a job + 3 candidates with resumes and pre-computed evaluations (no LLM/quota),
so the deployed app shows populated search + radar charts immediately.

### 6. Wire the frontend to the API
Open **`airi-api`** → copy its URL (e.g. `https://airi-api.onrender.com`). Open
**`airi-frontend`** → **Environment** → set `AIRI_API_URL` to that URL → save (redeploys).

### 7. Verify
- `airi-api` URL + `/health` → healthy; `/docs` → Swagger.
- `airi-frontend` URL → dashboard shows 🟢 Healthy + counts; try **Search** and open a
  candidate to see the radar/scorecard.

Put both URLs on your resume/README. (First hit after idle wakes the free service.)

## Notes
- **Uploads** work in sync mode (the pipeline runs inline in the request; first upload is
  slower because the embedding model downloads once per container).
- **LLM features** (evaluation, copilot) use your Gemini key; on free-tier `429`, wait or
  enable billing — the app degrades gracefully.
- **Async worker (optional):** uncomment the worker block in `render.yaml`, set
  `INGEST_MODE=async`, add a Redis (Upstash) URL to the secrets, and use a paid worker plan.

## Troubleshooting
- **Migrate fails** → check `DATABASE_URL` (prefix `postgresql+psycopg://`,
  `channel_binding=disable`); the Neon role must allow `CREATE EXTENSION vector`.
- **Frontend "API offline"** → `AIRI_API_URL` wrong/unset, or the free API is cold-starting
  (retry ~30s).
- **LLM 503** → `GEMINI_API_KEY` not set. **429** → Gemini free-tier quota.
