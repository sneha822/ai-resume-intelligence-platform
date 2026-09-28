"""AI Resume Intelligence — landing page / dashboard."""

from __future__ import annotations

import streamlit as st
import theme
from api_client import APIError
from common import get_client

st.set_page_config(page_title="AI Resume Intelligence", page_icon="🧭", layout="wide")
theme.inject()

client = get_client()

# --- Hero -------------------------------------------------------------------
theme.hero(
    title="AI Resume Intelligence",
    tag="AI HIRING COPILOT",
    lead=(
        "Upload resumes and let AI do the screening. Search your candidate pool by "
        "meaning (not just keywords), score each person against a job with an "
        "explainable rubric, and chat with an assistant grounded in your own data."
    ),
)

# --- Live metrics -----------------------------------------------------------
try:
    healthy = client.health().get("status") == "healthy"
except APIError:
    healthy = False

candidates: list = []
jobs: list = []
if healthy:
    try:
        candidates = client.list_candidates()
        jobs = client.list_jobs()
    except APIError:
        pass

c1, c2, c3 = st.columns(3)
c1.markdown(
    theme.metric_card("API status", "🟢 Healthy" if healthy else "🔴 Offline"),
    unsafe_allow_html=True,
)
c2.markdown(theme.metric_card("Candidates", str(len(candidates))), unsafe_allow_html=True)
c3.markdown(theme.metric_card("Job postings", str(len(jobs))), unsafe_allow_html=True)

if not healthy:
    st.info(
        "The API is waking up (free hosting sleeps when idle) — refresh in ~30s. "
        "Or start it locally with `python -m backend`."
    )

# --- How it works -----------------------------------------------------------
st.markdown('<div class="eyebrow">How it works</div>', unsafe_allow_html=True)
s1, s2, s3 = st.columns(3)
s1.markdown(
    theme.step_card(
        1,
        "Ingest resumes",
        "PDFs are parsed and an LLM extracts the name, skills, and experience — then each resume is embedded for search.",
    ),
    unsafe_allow_html=True,
)
s2.markdown(
    theme.step_card(
        2,
        "Search & shortlist",
        "Find candidates by meaning using hybrid search: dense vector embeddings + keyword BM25, fused with reciprocal rank fusion.",
    ),
    unsafe_allow_html=True,
)
s3.markdown(
    theme.step_card(
        3,
        "Evaluate & explain",
        "Score a candidate against a job on a 4-part rubric with reasoning, a fit level, and a competency radar.",
    ),
    unsafe_allow_html=True,
)

# --- Features ---------------------------------------------------------------
st.markdown('<div class="eyebrow">What you can do</div>', unsafe_allow_html=True)
f1, f2 = st.columns(2)
f1.markdown(
    theme.feature_card(
        "🔎",
        "Hybrid semantic search",
        "Dense + keyword retrieval so “built transformers” matches a search for “NLP experience.”",
    ),
    unsafe_allow_html=True,
)
f2.markdown(
    theme.feature_card(
        "📊",
        "Explainable evaluation",
        "A rubric score with per-criterion reasoning, gap analysis, and a radar chart — not an opaque number.",
    ),
    unsafe_allow_html=True,
)
f3, f4 = st.columns(2)
f3.markdown(
    theme.feature_card(
        "💬",
        "Recruiting copilot",
        "Ask questions about your candidates and get grounded, streaming answers.",
    ),
    unsafe_allow_html=True,
)
f4.markdown(
    theme.feature_card(
        "🔌",
        "Multi-provider AI",
        "Runs on Claude, Gemini, or a local model — swappable by config, no code change.",
    ),
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Get started</div>', unsafe_allow_html=True)
st.markdown(
    "Use the sidebar → **Search** to find candidates, **Candidates** for the deep-dive "
    "and competency radar, **Jobs** to manage roles, or **Copilot** to ask questions."
)

st.markdown(
    '<div class="foot">Built with FastAPI · PostgreSQL + pgvector · fastembed · '
    "Gemini/Claude · Streamlit — a domain-driven, ports-&-adapters architecture.</div>",
    unsafe_allow_html=True,
)
