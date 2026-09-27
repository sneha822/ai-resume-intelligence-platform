"""AI Resume Intelligence — frontend home / dashboard."""

from __future__ import annotations

import streamlit as st
import theme
from api_client import APIError
from common import get_client

st.set_page_config(page_title="AI Resume Intelligence", page_icon="🧭", layout="wide")

theme.page_header(
    "AI Resume Intelligence",
    "Hybrid semantic search, rubric evaluation, and a recruiting copilot.",
)

client = get_client()

col1, col2, col3 = st.columns(3)
try:
    health = client.health()
    connected = health.get("status") == "healthy"
except APIError as exc:
    connected = False
    st.error(f"Backend unreachable: {exc.detail}")

if connected:
    try:
        candidates = client.list_candidates()
        jobs = client.list_jobs()
    except APIError as exc:
        candidates, jobs = [], []
        st.warning(f"Could not load data: {exc.detail}")

    col1.metric("API", "🟢 Healthy")
    col2.metric("Candidates", len(candidates))
    col3.metric("Job postings", len(jobs))

    st.markdown("---")
    st.subheader("Get started")
    st.markdown(
        "- **Search** — hybrid dense + keyword candidate search\n"
        "- **Candidates** — deep-dive, competency radar, side-by-side compare\n"
        "- **Jobs** — manage job postings\n"
        "- **Copilot** — ask grounded questions about your candidates\n\n"
        "Use the sidebar to navigate."
    )
else:
    col1.metric("API", "🔴 Offline")
    st.info(
        "Start the backend first:  `python -m backend`  "
        "(set `AIRI_API_URL` if it runs elsewhere)."
    )
