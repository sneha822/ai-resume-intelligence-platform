"""Job postings management."""

from __future__ import annotations

import streamlit as st
import theme
from api_client import APIError
from common import get_client

theme.page_header("Jobs", "Create and browse job postings.")

client = get_client()

with st.form("create_job", clear_on_submit=True):
    title = st.text_input("Title", placeholder="Senior ML Engineer")
    description = st.text_area("Description", placeholder="Responsibilities, required skills, ...")
    submitted = st.form_submit_button("Create job", type="primary")
    if submitted:
        if title.strip() and description.strip():
            try:
                client.create_job(title, description)
                st.success("Job created.")
            except APIError as exc:
                st.error(f"Create failed: {exc.detail}")
        else:
            st.warning("Title and description are required.")

st.markdown("---")
st.subheader("Existing jobs")
try:
    jobs = client.list_jobs()
except APIError as exc:
    st.error(exc.detail)
    jobs = []

if not jobs:
    st.caption("No jobs yet.")
for j in jobs:
    st.markdown(
        f'<div class="airi-card"><b>{j["title"]}</b><br>'
        f'<span class="airi-muted">{j["description"][:200]}</span></div>',
        unsafe_allow_html=True,
    )
