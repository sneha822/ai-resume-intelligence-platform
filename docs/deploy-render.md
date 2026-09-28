# Deploy to Render (step by step)

This deploys the **API + Celery worker + Streamlit frontend** from your GitHub repo
using the `render.yaml` Blueprint. Your data stays on **Neon** (Postgres+pgvector) and
**Upstash** (Redis). No local Docker needed — Render builds the images.

**Cost note:** API and frontend run on Render's **free** web plan (they sleep after ~15
min idle and cold-start on the next request). The **Celery worker requires a paid plan**
(Render has no free background worker; ~$7/mo "starter"). If you want to stay free, you
can skip the worker — see "Free-only option" at the end.

---

## Prerequisites (you already have these)
- Neon `DATABASE_URL`, Upstash `rediss://` URL, and a `GEMINI_API_KEY` (from your `.env`).
- The repo pushed to GitHub (it is).

## Steps

### 1. Create a Render account
Go to <https://render.com> → **Sign up with GitHub**. Authorize Render to read your repos.

### 2. Create the Blueprint
- Dashboard → **New +** → **Blueprint**.
- Pick your repo `sneha822/ai-resume-intelligence-platform`, branch `main`.
- Render reads `render.yaml` and shows 3 services (`airi-api`, `airi-worker`,
  `airi-frontend`) + an env group (`airi-secrets`). Click **Apply**.

### 3. Fill in the secrets
Render will prompt for every `sync: false` value (nothing secret is in git). Paste:

**In the `airi-secrets` env group:**
| Key | Value |
|---|---|
| `DATABASE_URL` | `postgresql+psycopg://<user>:<pass>@<neon-host>/<db>?sslmode=require&channel_binding=disable` |
| `REDIS_URL` | `rediss://default:<pass>@<upstash-host>:6379/0?ssl_cert_reqs=required` |
| `CELERY_BROKER_URL` | same Upstash `rediss://` URL |
| `CELERY_RESULT_BACKEND` | same Upstash `rediss://` URL |
| `GEMINI_API_KEY` | your Gemini key |

> Use the **exact** Neon string with `channel_binding=disable` and the `postgresql+psycopg://`
> prefix (not plain `postgresql://`). Use the Upstash **`rediss://`** (TLS) URL.

### 4. First deploy
Click **Create/Apply**. Render builds and starts the services. Watch the **`airi-api`**
logs — on boot it runs `alembic upgrade head` (creating tables + the pgvector extension on
Neon if not already there) then starts uvicorn. Wait for "healthy".

### 5. Wire the frontend to the API
- Open the **`airi-api`** service → copy its URL (e.g. `https://airi-api.onrender.com`).
- Open **`airi-frontend`** → **Environment** → set `AIRI_API_URL` to that URL → save
  (it redeploys).

### 6. Verify
- Open the **`airi-api`** URL + `/health` → `{"status":"healthy",...}` and `/docs` for Swagger.
- Open the **`airi-frontend`** URL → the dashboard should show 🟢 Healthy + your counts.
- Try **Search** and **Copilot** in the UI. Upload a resume (needs the worker running).

---

## Ingest resumes
- **With the worker (paid):** use the UI "upload" or `POST /api/v1/resumes` — it queues to
  Upstash and the worker processes it.
- **Anytime (no worker):** run the ingest script locally against the same Neon DB:
  ```bash
  .venv/Scripts/python -c "import base64,glob,os; from backend.workers.tasks import ingest_resume; [ingest_resume(os.path.basename(p), base64.b64encode(open(p,'rb').read()).decode()) for p in glob.glob('legacy/data/raw/*.pdf')]"
  ```
  (Runs the pipeline directly; writes to the same Neon DB your deployed app reads.)

## Free-only option (skip the paid worker)
In `render.yaml`, delete the `airi-worker` service block, commit, and re-sync the Blueprint.
Everything except async upload works (search, single + batch evaluation, copilot). Ingest
via the script above.

## Troubleshooting
- **API deploy fails on migrate** → check `DATABASE_URL` (prefix `postgresql+psycopg://`,
  `channel_binding=disable`), and that the Neon role can `CREATE EXTENSION vector`.
- **Worker can't reach Redis** → use the `rediss://` (TLS) URL with `?ssl_cert_reqs=required`.
- **Frontend shows "API offline"** → `AIRI_API_URL` is wrong/unset, or the free API is
  cold-starting (retry after ~30s).
- **LLM endpoints return 503** → `GEMINI_API_KEY` not set in the env group.
- **429 from Gemini** → free-tier quota; wait or enable billing.
- **Free service is slow first hit** → free web services sleep when idle; the first request
  wakes them (cold start).
