"""Hybrid candidate search."""

from __future__ import annotations

import streamlit as st
import theme
from api_client import APIError
from common import get_client

theme.page_header("Search", "Dense embeddings + BM25, fused with reciprocal rank fusion.")

client = get_client()

query = st.text_input(
    "Search candidates", placeholder="e.g. senior NLP engineer with RAG experience"
)
top_k = st.slider("Results", min_value=1, max_value=25, value=10)

if st.button("Search", type="primary") and query.strip():
    try:
        results = client.search(query, top_k=top_k)
    except APIError as exc:
        st.error(f"Search failed: {exc.detail}")
        results = []

    if not results:
        st.info("No matches. Ingest resumes first.")
    else:
        # Resolve names for nicer display.
        try:
            names = {
                c["id"]: (c.get("name") or c.get("email") or c["id"][:8])
                for c in client.list_candidates()
            }
        except APIError:
            names = {}
        st.caption(f"{len(results)} result(s), ranked by fused relevance")
        for i, hit in enumerate(results, start=1):
            cid = hit["candidate_id"]
            label = names.get(cid, cid[:8])
            st.markdown(
                f'<div class="airi-card"><b>#{i} &nbsp; {label}</b> '
                f'<span class="airi-muted">&nbsp; score {hit["score"]:.4f}</span><br>'
                f'<span class="airi-muted">candidate id: {cid}</span></div>',
                unsafe_allow_html=True,
            )
