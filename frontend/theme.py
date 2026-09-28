"""Shared theme: modern SaaS look via CSS design tokens + layout helpers."""

from __future__ import annotations

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --accent: #818cf8;
  --accent-2: #22d3ee;
  --card: rgba(255,255,255,0.03);
  --card-border: rgba(255,255,255,0.08);
  --muted: #9aa3b2;
  --radius: 16px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Hide Streamlit chrome for a product feel */
#MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1100px; }

/* Sidebar */
[data-testid="stSidebar"] { background: #0e131c; border-right: 1px solid var(--card-border); }

/* Hero */
.hero {
  border-radius: 22px;
  padding: 2.4rem 2.2rem;
  background:
    radial-gradient(1200px 300px at 10% -20%, rgba(129,140,248,0.28), transparent 60%),
    radial-gradient(900px 300px at 90% 0%, rgba(34,211,238,0.18), transparent 55%),
    linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  border: 1px solid var(--card-border);
  margin-bottom: 1.4rem;
}
.hero h1 {
  font-size: 2.5rem; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 .4rem 0;
  background: linear-gradient(90deg, #fff, #c7cbff 60%, #7dd3fc);
  -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
}
.hero .tag { color: var(--accent); font-weight: 600; font-size: .95rem; letter-spacing: .02em; }
.hero p.lead { color: #cbd2df; font-size: 1.06rem; line-height: 1.6; margin: .6rem 0 0; max-width: 720px; }

.eyebrow { color: var(--muted); font-weight:600; text-transform: uppercase; letter-spacing:.12em; font-size:.72rem; margin: 1.6rem 0 .6rem; }

/* Cards */
.card {
  border: 1px solid var(--card-border); border-radius: var(--radius);
  padding: 1.1rem 1.2rem; background: var(--card); height: 100%;
}
.card .ico { font-size: 1.5rem; }
.card h3 { margin: .5rem 0 .3rem; font-size: 1.05rem; font-weight: 700; }
.card p { color: var(--muted); font-size: .9rem; line-height: 1.5; margin: 0; }

/* Metric card */
.metric { border:1px solid var(--card-border); border-radius: var(--radius); padding: 1rem 1.2rem; background: var(--card); }
.metric .label { color: var(--muted); font-size:.8rem; font-weight:600; text-transform:uppercase; letter-spacing:.08em; }
.metric .value { font-size: 1.9rem; font-weight: 800; letter-spacing:-.02em; margin-top:.15rem; }

/* Step */
.step { border:1px solid var(--card-border); border-radius: var(--radius); padding: 1rem 1.1rem; background: var(--card); height:100%; }
.step .n { display:inline-flex; align-items:center; justify-content:center; width:26px; height:26px; border-radius:50%;
  background: var(--accent); color:#0b0e14; font-weight:800; font-size:.85rem; }
.step h4 { margin:.5rem 0 .25rem; font-size:.98rem; }
.step p { color: var(--muted); font-size:.86rem; margin:0; line-height:1.45; }

.pill { display:inline-block; padding:.15rem .6rem; border-radius:999px; font-size:.78rem; font-weight:700; color:#fff; }
.airi-card { border:1px solid var(--card-border); border-radius:14px; padding:1rem 1.15rem; margin-bottom:.75rem; background:var(--card); }
.airi-muted { color: var(--muted); font-size:.88rem; }
.foot { color: var(--muted); font-size:.82rem; margin-top:2rem; border-top:1px solid var(--card-border); padding-top:1rem; }

/* Buttons */
.stButton > button {
  border-radius: 10px; font-weight:600; border:1px solid var(--card-border);
}
.stButton > button[kind="primary"] { background: var(--accent); border:none; color:#0b0e14; }

h1,h2,h3 { letter-spacing:-.01em; }
</style>
"""

_FIT_COLORS = {"strong": "#16a34a", "moderate": "#d97706", "weak": "#dc2626"}


def inject() -> None:
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, tag: str, lead: str) -> None:
    inject()
    st.markdown(
        f'<div class="hero"><div class="tag">{tag}</div>'
        f"<h1>{title}</h1><p class='lead'>{lead}</p></div>",
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "") -> None:
    inject()
    st.markdown(
        f'<div class="hero" style="padding:1.6rem 1.8rem"><h1 style="font-size:2rem">{title}</h1>'
        + (f'<p class="lead" style="margin-top:.2rem">{subtitle}</p>' if subtitle else "")
        + "</div>",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str) -> str:
    return f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div></div>'


def feature_card(icon: str, title: str, body: str) -> str:
    return f'<div class="card"><div class="ico">{icon}</div>' f"<h3>{title}</h3><p>{body}</p></div>"


def step_card(n: int, title: str, body: str) -> str:
    return f'<div class="step"><span class="n">{n}</span>' f"<h4>{title}</h4><p>{body}</p></div>"


def fit_badge(fit_level: str) -> str:
    color = _FIT_COLORS.get(fit_level.lower(), "#6b7280")
    return f'<span class="pill" style="background:{color}">{fit_level.upper()}</span>'
