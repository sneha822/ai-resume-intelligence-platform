"""Shared frontend helpers: cached API client and Plotly builders."""

from __future__ import annotations

from typing import Any

import plotly.graph_objects as go
import streamlit as st
from api_client import APIClient


@st.cache_resource
def get_client() -> APIClient:
    return APIClient()


def radar_figure(series: list[tuple[str, list[dict[str, Any]]]]) -> go.Figure:
    """Build a competency radar. ``series`` is a list of (label, rubric) where each
    rubric is a list of {criterion, score} dicts (0-10)."""
    fig = go.Figure()
    for label, rubric in series:
        criteria = [r["criterion"] for r in rubric]
        scores = [float(r["score"]) for r in rubric]
        if criteria:
            criteria.append(criteria[0])
            scores.append(scores[0])
        fig.add_trace(go.Scatterpolar(r=scores, theta=criteria, fill="toself", name=label))
    fig.update_layout(
        polar={"radialaxis": {"visible": True, "range": [0, 10]}},
        showlegend=len(series) > 1,
        margin={"l": 40, "r": 40, "t": 30, "b": 30},
        height=420,
    )
    return fig
