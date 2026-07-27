"""
AI Resume Intelligence Platform - Streamlit Dashboard
-----------------------------------------------------
Consolidated user interface for extracting resume data, inspecting
candidate metrics, searching applicant profiles, and viewing system specs.
"""

import os
import sys
from typing import Optional

import pandas as pd
import streamlit as st

# ----------------------------------------------------------
# Environment Setup & Path Resolution
# ----------------------------------------------------------
# Ensure root workspace directory is accessible in Python Path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.file_handler import FileHandler
from src.parser import ResumeParser

# ----------------------------------------------------------
# Configuration Constants
# ----------------------------------------------------------
DATASET_PATH = os.path.join(ROOT_DIR, "data", "processed_candidates.csv")
TEMP_UPLOAD_DIR = os.path.join(ROOT_DIR, "data", "temp_uploads")


# ----------------------------------------------------------
# Helper Data Loaders
# ----------------------------------------------------------
def load_candidate_dataset(file_path: str = DATASET_PATH) -> Optional[pd.DataFrame]:
    """
    Safely loads candidate dataset records from CSV.

    Args:
        file_path (str): Filepath to processed candidates CSV.

    Returns:
        Optional[pd.DataFrame]: Pandas DataFrame if successful, else None.
    """
    if os.path.exists(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as err:
            st.warning(f"Could not load dataset: {err}")
            return None
    return None


# ----------------------------------------------------------
# Page Configuration & Custom CSS
# ----------------------------------------------------------
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px !important;
        font-weight: 800 !important;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 16px !important;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .section-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------
# Core Subsystem Initialization & Dataset Metrics
# ----------------------------------------------------------
file_handler = FileHandler()
resume_parser = ResumeParser()
df_candidates = load_candidate_dataset()

# Calculate dynamic dataset metrics cleanly
if df_candidates is not None and not df_candidates.empty:
    total_candidates = len(df_candidates)
    avg_skills = (
        round(df_candidates["skill_count"].mean(), 1)
        if "skill_count" in df_candidates.columns
        else "N/A"
    )
    avg_exp = (
        round(df_candidates["experience_years"].mean(), 1)
        if "experience_years" in df_candidates.columns
        else "N/A"
    )
    advanced_candidates = (
        len(df_candidates[df_candidates["candidate_level"] == "Advanced"])
        if "candidate_level" in df_candidates.columns
        else "N/A"
    )
else:
    total_candidates = 0
    avg_skills = "N/A"
    avg_exp = "N/A"
    advanced_candidates = "N/A"

# ----------------------------------------------------------
# Sidebar Control Panel
# ----------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛠️ Control Panel")
    st.caption("Day 25 • Codebase & UI Optimization")
    st.markdown("---")

    st.markdown("### Engine Settings")
    parse_engine = st.selectbox(
        "Parsing Engine", ["Rule-Based (Fast)", "Advanced NLP (Coming Soon)"]
    )
    enable_scoring = st.checkbox("Apply Scoring Engine", value=True)

    st.markdown("---")
    st.caption("AI Resume Intelligence Platform v1.0 • 2026")

# ----------------------------------------------------------
# Header & Dynamic Metrics Overview
# ----------------------------------------------------------
st.markdown(
    '<p class="main-title">📄 AI Resume Intelligence Platform</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="subtitle">Extract structural insights, calculate feature metrics, and search applicant analytics dynamically.</p>',
    unsafe_allow_html=True,
)

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric(label="Total Candidates", value=str(total_candidates))

with metric_col2:
    st.metric(label="Average Skills", value=str(avg_skills))

with metric_col3:
    st.metric(
        label="Average Experience",
        value=f"{avg_exp} yrs" if avg_exp != "N/A" else "N/A",
    )

with metric_col4:
    st.metric(label="Advanced Candidates", value=str(advanced_candidates))

st.markdown("---")

# ----------------------------------------------------------
# Main Application Workspace Tabs
# ----------------------------------------------------------
tab_upload, tab_analytics, tab_search, tab_docs = st.tabs(
    [
        "📤 Resume Upload",
        "📊 Candidate Analytics",
        "🔍 Search Candidates",
        "ℹ️ About & Docs",
    ]
)

# TAB 1: Intake & Resume Parsing
with tab_upload:
    st.markdown("### 🚀 Candidate Intake & Parsing")

    uploaded_files = st.file_uploader(
        "Drop candidate resumes here (TXT or PDF format)",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.success(f"Staged {len(uploaded_files)} file(s) for parsing.")

        if st.button("🔥 Run Parsing Pipeline"):
            with st.spinner("Processing structural feature extractions..."):
                for uploaded_file in uploaded_files:
                    try:
                        saved_path = file_handler.save_uploaded_file(
                            uploaded_file, TEMP_UPLOAD_DIR
                        )

                        if uploaded_file.type == "text/plain":
                            file_content = uploaded_file.getvalue().decode("utf-8")
                            with st.expander(f"👀 Preview: {uploaded_file.name}"):
                                st.text(file_content[:1000])

                        parsed_data = resume_parser.parse_resume(saved_path)

                        st.markdown(f"#### 📄 Extract: `{uploaded_file.name}`")
                        st.json(parsed_data)

                        skills_count = len(parsed_data.get("skills", []))
                        st.metric(
                            label="⚡ Precision Extraction",
                            value=f"{skills_count} Skills Found",
                            delta=(
                                "Match Found" if skills_count > 0 else "No Skills"
                            ),
                        )
                        st.markdown("---")

                    except Exception as err:
                        st.error(f"Error parsing `{uploaded_file.name}`: {err}")

                st.success("Pipeline parsing complete!")
    else:
        st.info("💡 Select or drop candidate resumes above to start extraction.")

# TAB 2: Candidate Dataset Analytics
with tab_analytics:
    st.markdown("### 📊 Dataset Overview")

    if df_candidates is not None and not df_candidates.empty:
        st.dataframe(df_candidates, use_container_width=True)

        st.markdown("#### Feature Matrix Summary")
        numeric_columns = df_candidates.select_dtypes(include=["number"])
        if not numeric_columns.empty:
            st.dataframe(numeric_columns.describe(), use_container_width=True)
    else:
        st.warning(f"No candidate dataset found at `{DATASET_PATH}`.")

# TAB 3: Skill & Keyword Candidate Search
with tab_search:
    st.markdown("### 🔍 Search Candidate Profiles")

    search_query = st.text_input(
        "Enter keyword or skill (e.g., Python, SQL, Machine Learning):"
    )

    if search_query:
        if df_candidates is not None and not df_candidates.empty:
            search_results = df_candidates[
                df_candidates["skills"]
                .astype(str)
                .str.contains(search_query, case=False, na=False)
            ]

            if not search_results.empty:
                st.write(
                    f"Found **{len(search_results)}** matching candidate(s):"
                )
                st.dataframe(search_results, use_container_width=True)
            else:
                st.info(f"No candidates matching '{search_query}'.")
        else:
            st.warning("Candidate database currently unavailable.")

# TAB 4: Architecture & Documentation
with tab_docs:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🧩 System Architecture Overview")
    st.write(
        """
        The AI Resume Intelligence Platform extracts structured attributes from unstructured 
        resumes, computes numerical feature records, and outputs normalized datasets for downstream ML training.
        """
    )

    st.markdown("#### Core Execution Modules:")
    st.markdown(
        """
        * **Extraction Pipeline:** Standardizes input files and parses schema values.
        * **Feature Engineering:** Quantifies experience metrics and skill counts.
        * **Data Splitter:** Prepares training (`train_candidates.csv`) and evaluation splits.
        * **Search Engine:** Performs instant filtering on extracted skill features.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)