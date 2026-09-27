"""Recruiter copilot chat."""

from __future__ import annotations

import streamlit as st
import theme
from api_client import APIError
from common import get_client

theme.page_header("Copilot", "Ask grounded questions about your candidates.")

client = get_client()

try:
    candidates = client.list_candidates()
except APIError as exc:
    st.error(exc.detail)
    candidates = []

label_by_id = {c["id"]: (c.get("name") or c.get("email") or c["id"][:8]) for c in candidates}
selected = st.multiselect(
    "Candidate context (optional)",
    options=list(label_by_id),
    format_func=lambda i: label_by_id[i],
)

if "chat" not in st.session_state:
    st.session_state.chat = []

for role, msg in st.session_state.chat:
    with st.chat_message(role):
        st.markdown(msg)

prompt = st.chat_input("Ask about these candidates...")
if prompt:
    st.session_state.chat.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            resp = client.copilot(prompt, selected)
            answer = resp["answer"]
        except APIError as exc:
            answer = f"⚠️ {exc.detail}"
        st.markdown(answer)
    st.session_state.chat.append(("assistant", answer))
