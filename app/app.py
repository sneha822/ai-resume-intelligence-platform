import os
import sys

# MUST come before importing any 'src' modules
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

import pandas as pd
import streamlit as st
from src.ai.copilot import RecruiterCopilot
from src.ai.v2_pipeline import V2RecruitingPipeline
from src.file_handler import FileHandler
from src.parser import ResumeParser
from src.interview_question_generator import InterviewQuestionGenerator
from src.interview_report import InterviewReportGenerator
from src.scoring import CandidateScorer
from src.skill_recommender import SkillRecommendationEngine
from src.job_description import JobDescriptionParser
from src.batch_evaluator import BatchCandidateEvaluator


# ==========================================================
# 1. Page Configuration & Session State
# ==========================================================

st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State variables
if "parsed_skills" not in st.session_state:
    st.session_state["parsed_skills"] = []

if "latest_parsed_data" not in st.session_state:
    st.session_state["latest_parsed_data"] = None

if "leaderboard" not in st.session_state:
    st.session_state["leaderboard"] = pd.DataFrame()

if "v2_pipeline" not in st.session_state:
    st.session_state["v2_pipeline"] = V2RecruitingPipeline()

if "copilot" not in st.session_state:
    st.session_state["copilot"] = RecruiterCopilot()

v2_pipeline = st.session_state["v2_pipeline"]
copilot = st.session_state["copilot"]


# ==========================================================
# 2. Custom CSS Styling
# ==========================================================

st.markdown("""
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
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. Component Initialization
# ==========================================================

file_handler = FileHandler()
resume_parser = ResumeParser()
question_generator = InterviewQuestionGenerator()
report_generator = InterviewReportGenerator()
candidate_scorer = CandidateScorer()
skill_engine = SkillRecommendationEngine()
jd_parser = JobDescriptionParser()
batch_evaluator = BatchCandidateEvaluator()


# ==========================================================
# 4. Helper Functions
# ==========================================================

def display_candidate_metrics(leaderboard: pd.DataFrame):
    """Display summary metrics dynamically from evaluated candidate leaderboard."""
    if leaderboard.empty:
        st.info("No candidate data available yet.")
        return

    # Handle status breakdown cleanly
    if "status" in leaderboard.columns:
        successful = leaderboard[leaderboard["status"] == "Success"]
        failed = leaderboard[leaderboard["status"] == "Failed"]
    else:
        successful = leaderboard
        failed = pd.DataFrame()

    total_candidates = len(leaderboard)
    successful_count = len(successful)
    failed_count = len(failed)

    if successful_count > 0:
        average_score = successful["match_score"].mean()
        top_score = successful["match_score"].max()
    else:
        average_score = 0.0
        top_score = 0.0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Candidates", total_candidates)
    with col2:
        st.metric("Successfully Evaluated", successful_count)
    with col3:
        st.metric("Average Match Score", f"{average_score:.1f}%")
    with col4:
        st.metric("Top Match Score", f"{top_score:.1f}%")

    if failed_count > 0:
        st.warning(f"⚠️ {failed_count} candidate(s) encountered processing issues.")


# ==========================================================
# 5. Sidebar Control Panel
# ==========================================================

with st.sidebar:
    st.markdown("## 🛠️ Control Panel")
    st.caption("AI Resume Intelligence Platform v1.0")
    st.markdown("---")
    
    st.markdown("### ⚙️ Configuration")
    parse_mode = st.selectbox(
        "Parsing Engine",
        ["Rule-Based (Fast)", "Advanced NLP (Coming Soon)"]
    )

    enable_scoring = st.checkbox(
        "Enable Candidate Scoring",
        value=True
    )

    st.markdown("---")
    st.markdown("### 📌 Active Pipeline Subsystems")
    st.write("✓ Resume Parsing & Extraction")
    st.write("✓ JD Keyword Extraction")
    st.write("✓ Skill & Token Matching")
    st.write("✓ Similarity Scoring")
    st.write("✓ Candidate Ranking Leaderboard")
    st.write("✓ Batch Evaluator Engine")
    st.write("✓ Recruiter Copilot (LLM Search & QA)")
    st.write("✓ Evidence-Based Interview Question Generator")
    
    st.markdown("---")
    st.caption("AI Resume Intelligence Platform • 2026")


# ==========================================================
# 6. Header Layout
# ==========================================================

st.markdown(
    '<p class="main-title">📄 AI Resume Intelligence & Candidate Copilot</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">'
    'Extract core insights, score applicant profiles against job specifications, '
    'and generate candidate comparison leaderboards in real time.'
    '</p>',
    unsafe_allow_html=True
)


# ==========================================================
# 7. Interactive Workspace (Tabs)
# ==========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📤 Analyze Candidates",
        "🏗️ System Architecture",
        "📚 Platform Documentation"
    ]
)


# ==========================================================
# TAB 1: Candidate Intake & Evaluation Dashboard
# ==========================================================

with tab1:
    st.markdown("### 🚀 Candidate Resume Intake")

    col_up1, col_up2 = st.columns(2)

    with col_up1:
        uploaded_files = st.file_uploader(
            "Upload Candidate Resumes (PDF or TXT)",
            type=["txt", "pdf"],
            accept_multiple_files=True
        )

    with col_up2:
        jd_file = st.file_uploader(
            "Upload Job Description (TXT)",
            type=["txt"],
            key="job_description_upload"
        )

    if uploaded_files:
        st.success(f"📌 {len(uploaded_files)} candidate resume(s) staged.")
    if jd_file:
        st.success(f"🎯 Job Description loaded: {jd_file.name}")

    if uploaded_files and jd_file:
        if st.button("🚀 Run Candidate Intelligence Pipeline", type="primary"):
            with st.spinner("Processing batch evaluation and generating candidate matches..."):
                upload_dir = "data/temp_uploads"
                saved_resume_paths = []

                # Reset session states for current batch
                st.session_state["parsed_skills"] = []

                # Parse JD
                try:
                    jd_text = jd_file.getvalue().decode("utf-8")
                    jd_data = jd_parser.parse_job_description(jd_text)
                    job_keywords = jd_data.get("keywords", [])
                except Exception as error:
                    st.error(f"Failed to parse Job Description: {str(error)}")
                    job_keywords = []

                # Save candidate resumes locally for evaluator processing
                for uploaded_file in uploaded_files:
                    try:
                        saved_path = file_handler.save_uploaded_file(uploaded_file, upload_dir)
                        saved_resume_paths.append(saved_path)

                        # Set latest parsed preview state
                        parsed_data = resume_parser.parse_resume(saved_path)
                        st.session_state["latest_parsed_data"] = parsed_data

                        for skill in parsed_data.get("skills", []):
                            if skill.lower() not in st.session_state["parsed_skills"]:
                                st.session_state["parsed_skills"].append(skill.lower())

                    except Exception as error:
                        st.error(f"Could not stage file {uploaded_file.name}: {str(error)}")

                # Execute Day 48 Batch Evaluation Pipeline
                if saved_resume_paths and job_keywords:
                    st.session_state["leaderboard"] = batch_evaluator.evaluate_batch(
                        saved_resume_paths,
                        job_keywords
                    )
                    st.success("✨ Pipeline execution complete!")

    elif uploaded_files and not jd_file:
        st.info("💡 Please upload a Job Description to enable scoring and leaderboard calculation.")

    # ------------------------------------------------------
    # Results & Leaderboard Presentation
    # ------------------------------------------------------
    leaderboard = st.session_state.get("leaderboard")

    if leaderboard is not None and not leaderboard.empty:
        st.markdown("---")
        st.markdown("## 🏆 Candidate Intelligence Dashboard")
        
        display_candidate_metrics(leaderboard)
        st.markdown("---")

        if "status" in leaderboard.columns:
            successful_candidates = leaderboard[leaderboard["status"] == "Success"]
            failed_candidates = leaderboard[leaderboard["status"] == "Failed"]
        else:
            successful_candidates = leaderboard
            failed_candidates = pd.DataFrame()

        st.markdown("### 📊 Ranking Leaderboard")
        if not successful_candidates.empty:
            display_cols = ["rank", "candidate", "email", "match_score", "similarity_score"]
            avail_cols = [c for c in display_cols if c in successful_candidates.columns]

            st.dataframe(
                successful_candidates[avail_cols],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No successful candidate evaluations to rank.")

        # Recruiter Detailed Breakdown & Explainer Section
        if not successful_candidates.empty:
            st.markdown("### 🔎 Recruiter Candidate Inspector")
            
            selected_candidate = st.selectbox(
                "Select Candidate to View Breakdown:",
                successful_candidates["candidate"].tolist()
            )

            selected_row = successful_candidates[
                successful_candidates["candidate"] == selected_candidate
            ].iloc[0]

            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                st.markdown("#### ✅ Matched Skills")
                matched_str = selected_row.get("matched_skills", "")
                if matched_str and isinstance(matched_str, str):
                    for skill in matched_str.split(", "):
                        if skill:
                            st.success(f"✓ {skill}")
                else:
                    st.write("No matching skills detected.")

            with col_exp2:
                st.markdown("#### ⚠️ Missing Skills")
                missing_str = selected_row.get("missing_skills", "")
                if missing_str and isinstance(missing_str, str):
                    for skill in missing_str.split(", "):
                        if skill:
                            st.warning(f"⚠️ {skill}")
                else:
                    st.success("No major missing skill gaps!")

            # Score Comparison Visual Chart
            st.markdown("### 📈 Match Score Comparison")
            chart_data = (
                successful_candidates[["candidate", "match_score"]]
                .set_index("candidate")
            )
            st.bar_chart(chart_data)

        # Failed Candidates Safeguard Report
        if not failed_candidates.empty:
            st.markdown("---")
            st.warning(f"⚠️ {len(failed_candidates)} Candidate Evaluation(s) Failed")
            with st.expander("View Unprocessed File Logs"):
                for _, failed_row in failed_candidates.iterrows():
                    st.error(f"**{failed_row['candidate']}**: {failed_row.get('error', 'Processing exception')}")

        # ==========================================================
        # PART 7: Recruiter Copilot & Natural Language Search UI
        # ==========================================================
        st.markdown("---")
        st.subheader("🤖 Recruiter Copilot & Natural Language Search")
        st.write(
            "Search candidates using natural language "
            "and ask grounded questions about candidate evidence."
        )

        search_question = st.text_input(
            "Candidate search / question",
            placeholder="e.g. Find Python and AWS backend developers with at least 3 years of experience"
        )

        if st.button(" Ask Copilot", type="primary"):
            if not search_question.strip():
                st.warning("Please enter a question or search query.")
            else:
                with st.spinner("Copilot is analyzing candidate context..."):
                    # Convert leaderboard records into candidate list dictionary context
                    candidate_records = []
                    for idx, row in successful_candidates.iterrows():
                        candidate_records.append({
                            "candidate_id": row.get("candidate", f"Candidate_{idx}"),
                            "profile": row.to_dict()
                        })

                    try:
                        copilot_response = copilot.ask(search_question, candidate_records)
                        st.markdown("#### 💡 Copilot Response")
                        st.info(copilot_response)
                    except Exception as err:
                        st.error(f"Copilot failed to generate a response: {str(err)}")

        if copilot.conversation_history:
            with st.expander("📜 View Conversation History"):
                for turn in copilot.conversation_history:
                    role = turn.get("role", "user").capitalize()
                    content = turn.get("content", turn.get("question", turn.get("answer", "")))
                    if role == "User":
                        st.markdown(f"**🗣️ {role}:** {content}")
                    else:
                        st.markdown(f"**🤖 {role}:** {content}")
                if st.button("Clear History"):
                    copilot.clear_history()
                    st.experimental_rerun()

        # ==========================================================
        # PART 8: Candidate Evidence & Interview Question Generator
        # ==========================================================
        st.markdown("---")
        st.subheader("🎯 Evidence-Based Interview Question Generator")
        st.write("Generate targeted interview questions grounded in candidate profile evidence and missing skills.")

        selected_interview_candidate = st.selectbox(
            "Select Candidate for Interview Prep:",
            successful_candidates["candidate"].tolist(),
            key="interview_candidate_select"
        )

        if st.button("⚡ Generate Interview Questions", type="secondary"):
            candidate_row = successful_candidates[
                successful_candidates["candidate"] == selected_interview_candidate
            ].iloc[0]

            with st.spinner("Generating tailored technical and behavioral interview questions..."):
                try:
                    # Parse missing and matched skills lists
                    missing_skills_list = [
                        s.strip() for s in str(candidate_row.get("missing_skills", "")).split(",") if s.strip()
                    ]
                    matched_skills_list = [
                        s.strip() for s in str(candidate_row.get("matched_skills", "")).split(",") if s.strip()
                    ]

                    # Call question generator subsystem
                    questions = question_generator.generate_questions(
                        matched_skills=matched_skills_list,
                        missing_skills=missing_skills_list,
                        role=selected_interview_candidate
                    )

                    st.markdown(f"### 📋 Interview Guide for **{selected_interview_candidate}**")

                    if isinstance(questions, dict):
                        for category, q_list in questions.items():
                            st.markdown(f"#### 📌 {category.replace('_', ' ').title()}")
                            for q in q_list:
                                st.write(f"- {q}")
                    elif isinstance(questions, list):
                        for q in questions:
                            st.write(f"- {q}")
                    else:
                        st.write(questions)

                except Exception as err:
                    st.error(f"Failed to generate interview questions: {str(err)}")


# ==========================================================
# TAB 2: System Architecture & Workflow
# ==========================================================

with tab2:
    st.markdown("## 🏗️ End-to-End System Architecture")
    
    st.code("""
Candidate Resumes (PDF/TXT)            Job Description (TXT)
         │                                      │
         ▼                                      ▼
   File Handler                             JD Parser
         │                                      │
         ▼                                      ▼
   Resume Parser                        Keyword Extraction
  (Email, Phone, Skills)                        │
         │                                      │
         └──────────────────┬───────────────────┘
                            │
                            ▼
                   Batch Candidate Evaluator
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
         Token Matcher            Cosine Similarity
               │                         │
               └────────────┬────────────┘
                            │
                            ▼
                     Match Scorer Engine
                            │
                            ▼
                 Ranked Candidate Leaderboard
                            │
             ┌──────────────┴──────────────┐
             ▼                             ▼
   Recruiter AI Copilot        Interview Question Generator
             │                             │
             └──────────────┬──────────────┘
                            │
                            ▼
                 Streamlit Intelligence UI
    """, language="text")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🧩 Core System Component Responsibilities")
    st.markdown("""
    * **File Handler (`file_handler.py`):** Handles safe file ingest, stream buffering, and disk staging in `data/temp_uploads/`.
    * **Resume Parser (`parser.py`):** Extracts applicant email, phone, metadata, and normalizes skill entities.
    * **JD Parser (`job_description.py`):** Isolates target domain competencies and key requirements from candidate specs.
    * **Matcher & Scorer (`job_matcher.py` & `match_scorer.py`):** Calculates direct keyword intersection, precision, missing vectors, and similarity metrics.
    * **Batch Evaluator (`batch_evaluator.py`):** Coordinates multi-candidate evaluations with structured error handling so invalid files don't halt scoring.
    * **Recruiter Copilot (`copilot.py`):** Powers natural language candidate search and contextual QA over active profile data.
    * **Question Generator (`interview_question_generator.py`):** Synthesizes grounded technical and behavioral interview questions from candidate gap analysis.
    """)
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================================
# TAB 3: System Documentation & Guidelines
# ==========================================================

with tab3:
    st.markdown("## 📚 Platform Documentation")
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📖 User Operational Guide")
    st.markdown("""
    1. **Upload Input Files:** Under **Tab 1**, select candidate resumes (`.txt` or `.pdf`) along with your target Job Description (`.txt`).
    2. **Execute Analysis:** Click **Run Candidate Intelligence Pipeline** to start batch parsing, skill extraction, and scoring.
    3. **Review Metrics:** View total evaluations, success rates, average match ratios, and top candidate standings.
    4. **Inspect Gaps:** Use the **Recruiter Candidate Inspector** to review specific skill matches and missing requirements per candidate.
    5. **Query Copilot (Part 7):** Ask questions about candidates using natural language to extract evidence-backed summaries.
    6. **Generate Interview Guides (Part 8):** Select a candidate to auto-generate targeted technical and behavioral interview questions based on missing skill vectors.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🔧 API Subsystem Specifications")
    st.markdown("""
    * **Output Dataframe Schema:** `[rank, candidate, email, match_score, similarity_score, status, error]`
    * **Scoring Range:** Scaled normalized scores from `0.0%` to `100.0%`.
    * **Error Resilience Level:** Safe candidate exception handling during batch evaluation.
    """)