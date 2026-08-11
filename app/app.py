import os
import sys
import pandas as pd
import streamlit as st

# Ensure root workspace directory is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.file_handler import FileHandler
from src.parser import ResumeParser
from src.best_model import BestModelTrainer

# ==========================================================
# 1. Page Configuration
# ==========================================================
st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# 2. Dynamic Data Loading & Metrics
# ==========================================================
DATASET_PATH = "data/processed_candidates.csv"


def load_candidate_data():
    """Safely loads processed candidate dataset."""
    if os.path.exists(DATASET_PATH):
        try:
            return pd.read_csv(DATASET_PATH)
        except Exception:
            return None
    return None


df_candidates = load_candidate_data()

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

    if "candidate_level" in df_candidates.columns:
        beginner_count = len(
            df_candidates[df_candidates["candidate_level"] == "Beginner"]
        )
        intermediate_count = len(
            df_candidates[df_candidates["candidate_level"] == "Intermediate"]
        )
        advanced_count = len(
            df_candidates[df_candidates["candidate_level"] == "Advanced"]
        )
    else:
        beginner_count = intermediate_count = advanced_count = "N/A"
else:
    total_candidates = 0
    avg_skills = "N/A"
    avg_exp = "N/A"
    beginner_count = intermediate_count = advanced_count = "N/A"

# ==========================================================
# 3. Custom CSS Styling
# ==========================================================
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
    .card {
        background-color: #F8FAFC;
        padding: 18px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================================
# 4. Component Initialization
# ==========================================================
file_handler = FileHandler()
resume_parser = ResumeParser()
best_model = BestModelTrainer()

# ==========================================================
# 5. Sidebar Control Panel
# ==========================================================
with st.sidebar:
    st.markdown("## 🛠️ Control Panel")
    st.caption("Day 30 • Feature Inspection & Predictions")
    st.markdown("---")

    st.markdown("### Settings")
    parse_mode = st.selectbox(
        "Parsing Engine", ["Rule-Based (Fast)", "Advanced NLP (Coming Soon)"]
    )
    enable_scoring = st.checkbox("Apply Scoring Engine", value=True)

    st.markdown("---")
    st.caption("AI Resume Intelligence Platform v1.0 • 2026")

# ==========================================================
# 6. Header & Metrics Overview
# ==========================================================
st.markdown(
    '<p class="main-title">📄 AI Resume Intelligence Platform</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="subtitle">Extract core insights, calculate dynamic candidate metrics, and explore applicant analytics.</p>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Candidates", value=str(total_candidates))
with col2:
    st.metric(label="Average Skill Count", value=str(avg_skills))
with col3:
    st.metric(
        label="Average Experience",
        value=f"{avg_exp} yrs" if avg_exp != "N/A" else "N/A",
    )

st.markdown("---")

# ==========================================================
# 7. Workspace Tabs
# ==========================================================
tab_upload, tab_analytics, tab_search = st.tabs(
    ["📤 Upload & Analyze", "📊 Candidate Analytics", "🔍 Search Candidates"]
)

# ----------------------------------------------------------
# TAB 1: Upload & Formatted Candidate Analysis
# ----------------------------------------------------------
with tab_upload:
    st.markdown("### 🚀 Candidate Intake")

    uploaded_files = st.file_uploader(
        "Drop candidate resumes here (PDF or TXT format)",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.success(f"Staged {len(uploaded_files)} file(s) for parsing!")

        if st.button("🔥 Run Intelligence Pipeline"):
            with st.spinner("Processing structural extractions..."):
                upload_dir = "data/temp_uploads"

                for uploaded_file in uploaded_files:
                    try:
                        saved_path = file_handler.save_uploaded_file(
                            uploaded_file, upload_dir
                        )

                        if uploaded_file.type == "text/plain":
                            file_content = uploaded_file.getvalue().decode("utf-8")
                            with st.expander(f"👀 Raw Text Preview: {uploaded_file.name}"):
                                st.text(file_content[:1000])

                        # Core Parser Call
                        parsed_data = resume_parser.parse_resume(saved_path)

                        # Extract Candidate Features
                        skills_list = parsed_data.get("skills", [])
                        skill_count = len(skills_list) if isinstance(skills_list, list) else 0
                        exp_years = parsed_data.get("experience_years", 0)
                        project_count = parsed_data.get("project_count", 0)
                        cert_count = parsed_data.get("certification_count", 0)

                        candidate_features = [
                            skill_count,
                            exp_years,
                            project_count,
                            cert_count
                        ]

                        # Predict Candidate Outcome using saved Best Model
                        prediction = best_model.predict(candidate_features)

                        st.markdown("---")
                        st.markdown(f"## 📄 Candidate Profile: `{uploaded_file.name}`")

                        # Formatted Display Sections
                        col_left, col_right = st.columns(2)

                        with col_left:
                            # 1. Candidate Details
                            st.markdown("### 👤 Candidate Details")
                            st.write(f"**Email:** {parsed_data.get('email', 'N/A')}")
                            st.write(f"**Phone:** {parsed_data.get('phone', 'N/A')}")

                            # 2. Experience & Level
                            st.markdown("### 💼 Experience & Classification")
                            st.write(f"**Years of Experience:** {exp_years}")
                            st.write(
                                f"**Candidate Tier:** `{parsed_data.get('candidate_level', 'Unclassified')}`"
                            )

                        with col_right:
                            # 3. Skills
                            st.markdown("### ⚡ Extracted Skills")
                            if isinstance(skills_list, list) and len(skills_list) > 0:
                                for skill in skills_list:
                                    st.markdown(f"* {skill}")
                            elif isinstance(skills_list, str) and len(skills_list) > 0:
                                for skill in skills_list.split(","):
                                    st.markdown(f"* {skill.strip()}")
                            else:
                                st.write("No explicit skills detected.")

                        # 4. Key Numerical Highlights
                        st.markdown("### 📊 Key Numerical Highlights")
                        stat1, stat2, stat3 = st.columns(3)
                        with stat1:
                            st.metric(label="Skill Count", value=str(skill_count))
                        with stat2:
                            st.metric(label="Projects Identified", value=str(project_count))
                        with stat3:
                            st.metric(label="Certifications", value=str(cert_count))

                        # 5. STEP 9: Candidate Selection Outcome Prediction
                        st.markdown("### 🎯 Candidate Selection Prediction")
                        if str(prediction).lower() == "shortlisted":
                            st.success("✅ **Candidate Outcome: SHORTLISTED**")
                            st.caption("This candidate meets the benchmark criteria for initial selection.")
                        else:
                            st.warning("❌ **Candidate Outcome: REJECTED**")
                            st.caption("This profile does not currently meet the required selection threshold.")

                        # 6. STEP 10: Model Input Features Inspector
                        with st.expander("📊 Model Input Features"):
                            st.write({
                                "skill_count": candidate_features[0],
                                "experience_years": candidate_features[1],
                                "project_count": candidate_features[2],
                                "certification_count": candidate_features[3]
                            })

                        # 7. Raw JSON Data View
                        with st.expander("🔍 View Raw Parsed Data (JSON)"):
                            st.json(parsed_data)

                        st.markdown("---")

                    except Exception as error:
                        st.error(f"Error processing {uploaded_file.name}: {str(error)}")

                st.success("Pipeline processing complete!")

# ----------------------------------------------------------
# TAB 2 & 3: Analytics & Search
# ----------------------------------------------------------
with tab_analytics:
    st.markdown("### 📊 Dataset Summary")
    if df_candidates is not None and not df_candidates.empty:
        st.dataframe(df_candidates, use_container_width=True)
    else:
        st.warning("No dataset loaded at `data/processed_candidates.csv`.")

with tab_search:
    st.markdown("### 🔍 Search Candidates")
    query = st.text_input("Enter skill keyword (e.g. Python, SQL):")
    if query and df_candidates is not None and not df_candidates.empty:
        results = df_candidates[
            df_candidates["skills"]
            .astype(str)
            .str.contains(query, case=False, na=False)
        ]
        st.dataframe(results, use_container_width=True)