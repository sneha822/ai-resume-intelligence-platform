"""Shared theme: CSS design tokens + small helpers (dark-mode friendly)."""

from __future__ import annotations

import streamlit as st

# Design tokens (work against Streamlit's light/dark themes via CSS variables).
_CSS = """
<style>
:root {
  --airi-accent: #6366f1;
  --airi-accent-soft: rgba(99, 102, 241, 0.12);
  --airi-radius: 14px;
}
.airi-card {
  border: 1px solid rgba(128,128,128,0.25);
  border-radius: var(--airi-radius);
  padding: 1rem 1.15rem;
  margin-bottom: 0.75rem;
  background: var(--airi-accent-soft);
}
.airi-pill {
  display: inline-block; padding: 0.15rem 0.6rem; border-radius: 999px;
  font-size: 0.78rem; font-weight: 600; background: var(--airi-accent);
  color: white;
}
.airi-muted { opacity: 0.7; font-size: 0.85rem; }
h1, h2, h3 { letter-spacing: -0.01em; }
</style>
"""

_FIT_COLORS = {"strong": "#16a34a", "moderate": "#d97706", "weak": "#dc2626"}


def inject() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def fit_badge(fit_level: str) -> str:
    color = _FIT_COLORS.get(fit_level.lower(), "#6b7280")
    return f'<span class="airi-pill" style="background:{color}">' f"{fit_level.upper()}</span>"


def page_header(title: str, subtitle: str = "") -> None:
    inject()
    st.title(title)
    if subtitle:
        st.markdown(f'<p class="airi-muted">{subtitle}</p>', unsafe_allow_html=True)
