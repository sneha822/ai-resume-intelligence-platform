"""Candidate deep-dive, competency radar, scorecard, and side-by-side compare."""

from __future__ import annotations

import streamlit as st
import theme
from api_client import APIError
from common import get_client, radar_figure

theme.page_header("Candidates", "Deep-dive, competency radar, and side-by-side comparison.")

client = get_client()

try:
    candidates = client.list_candidates()
except APIError as exc:
    st.error(f"Could not load candidates: {exc.detail}")
    st.stop()

if not candidates:
    st.info("No candidates yet. Ingest resumes via the API (`POST /api/v1/resumes`).")
    st.stop()


def _label(c: dict) -> str:
    return c.get("name") or c.get("email") or c["id"][:8]


label_by_id = {c["id"]: _label(c) for c in candidates}

tab_detail, tab_compare = st.tabs(["Deep-dive", "Compare"])

with tab_detail:
    cid = st.selectbox("Candidate", options=list(label_by_id), format_func=lambda i: label_by_id[i])
    try:
        detail = client.get_candidate(cid)
    except APIError as exc:
        st.error(exc.detail)
        st.stop()

    st.subheader(_label(detail))
    st.caption(detail.get("email") or "no email on file")

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("**Resumes**")
        for r in detail.get("resumes", []):
            st.markdown(f"- {r['filename']}")
        st.markdown("**Profile sections**")
        sections = (detail.get("profile") or {}).get("sections", {})
        if sections:
            for name in sections:
                st.markdown(f"- {name}")
        else:
            st.caption("No parsed sections.")

    with c2:
        evals = detail.get("evaluations", [])
        if evals:
            latest = evals[-1]["result"]
            st.markdown(
                f"**Latest evaluation** &nbsp; {theme.fit_badge(latest['fit_level'])} "
                f"&nbsp; score **{latest['overall_score']:.0f}/100**",
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                radar_figure([(_label(detail), latest["rubric"])]),
                use_container_width=True,
            )
        else:
            st.info("No evaluation yet — run one against a job below.")
            jobs = client.list_jobs()
            if jobs:
                jid = st.selectbox(
                    "Job",
                    options=[j["id"] for j in jobs],
                    format_func=lambda i: next(j["title"] for j in jobs if j["id"] == i),
                )
                if st.button("Run evaluation", type="primary"):
                    try:
                        client.evaluate(cid, jid)
                        st.rerun()
                    except APIError as exc:
                        st.error(f"Evaluation failed: {exc.detail}")
            else:
                st.caption("Create a job first (Jobs page).")

    if evals:
        latest = evals[-1]["result"]
        st.markdown("### Interview scorecard")
        for rub in latest["rubric"]:
            st.markdown(
                f'<div class="airi-card"><b>{rub["criterion"]}</b> '
                f'<span class="airi-muted">&nbsp; {rub["score"]:.1f}/10</span><br>'
                f'{rub["reasoning"]}</div>',
                unsafe_allow_html=True,
            )
        gaps = latest.get("gaps", {})
        if gaps.get("recommendation"):
            st.success(f"Recommendation: {gaps['recommendation']}")

with tab_compare:
    picks = st.multiselect(
        "Pick 2+ candidates",
        options=list(label_by_id),
        format_func=lambda i: label_by_id[i],
        max_selections=4,
    )
    series = []
    for pid in picks:
        d = client.get_candidate(pid)
        evs = d.get("evaluations", [])
        if evs:
            series.append((_label(d), evs[-1]["result"]["rubric"]))
    if len(series) >= 2:
        st.plotly_chart(radar_figure(series), use_container_width=True)
    elif picks:
        st.info("Selected candidates need evaluations to compare competencies.")
