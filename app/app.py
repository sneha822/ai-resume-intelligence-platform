import os
import sys
import streamlit as st

# Fix Python path so 'src' modules can be imported when running from the app directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.file_handler import FileHandler  
from src.parser import ResumeParser 
from src.interview_question_generator import InterviewQuestionGenerator 
from src.interview_report import InterviewReportGenerator
from src.scoring import CandidateScorer  
from src.skill_recommender import SkillRecommendationEngine

# ==========================================================
# 1. Page Configuration & Session State
# ==========================================================
st.set_page_config(
    page_title="Resume Intelligence Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for cross-tab data persistence
if "parsed_skills" not in st.session_state:
    st.session_state["parsed_skills"] = []
if "processed_count" not in st.session_state:
    st.session_state["processed_count"] = 0
if "total_scores" not in st.session_state:
    st.session_state["total_scores"] = []
if "latest_parsed_data" not in st.session_state:
    st.session_state["latest_parsed_data"] = None

# ==========================================================
# 2. Custom CSS Styling
# ==========================================================
st.markdown("""
    <style>
    .main-title {
        font-size: 40px !important;
        font-weight: 800 !important;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px !important;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .section-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================================
# 3. Component Initialization (Part 5)
# ==========================================================
file_handler = FileHandler()
resume_parser = ResumeParser()
question_generator = InterviewQuestionGenerator()
report_generator = InterviewReportGenerator()
candidate_scorer = CandidateScorer()
skill_engine = SkillRecommendationEngine()

# ==========================================================
# 4. Sidebar Control Panel
# ==========================================================
with st.sidebar:
    st.markdown("## 🛠️ Control Panel")
    st.write("Week 3: Frontend Interface")
    st.markdown("---")
    
    st.markdown("### Settings")
    parse_mode = st.selectbox("Parsing Engine", ["Rule-Based (Fast)", "Advanced NLP (Coming Soon)"])
    enable_scoring = st.checkbox("Apply Day 14 Scoring Engine", value=True)
    
    st.markdown("---")
    st.caption("AI Resume Intelligence Platform v1.0 • 2026")

# ==========================================================
# 5. Header Layout & Dynamic Metrics
# ==========================================================
st.markdown('<p class="main-title">📄 AI Resume Intelligence & Interview Copilot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Extract core insights, rank candidate profiles, and generate intelligent interview pathways instantly.</p>', unsafe_allow_html=True)

# Calculate dynamic averages
processed_cnt = st.session_state["processed_count"]
avg_score_val = (
    f"{sum(st.session_state['total_scores']) / processed_cnt:.1f} pts" 
    if processed_cnt > 0 else "N/A"
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Processed Resumes", value=str(processed_cnt), delta="Active Session")
with col2:
    st.metric(label="Top Matching Track", value="Python / SQL", delta="Data Engineering")
with col3:
    st.metric(label="Avg Match Score", value=avg_score_val, delta="Live Score" if processed_cnt > 0 else "No data processed")

st.markdown("---")

# ==========================================================
# 6. Interactive Workspace (Tabs)
# ==========================================================
tab1, tab2, tab3 = st.tabs(
    [
        "📤 Upload & Analyze",
        "🎯 Interview Questions",
        "📋 Project Overview & Docs"
    ]
)

# ---------------------------------------------------------
# TAB 1: Upload & Analyze Only
# ---------------------------------------------------------
with tab1:
    st.markdown("### 🚀 Candidate Intake")
    
    uploaded_files = st.file_uploader(
        "Drop candidate resumes here (PDF, TXT, or DOCX format)", 
        type=["txt", "pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"Successfully staged {len(uploaded_files)} file(s) for parsing!")
        
        if st.button("🔥 Run Intelligence Pipeline"):
            with st.spinner("Executing structural extraction and scoring algorithms..."):
                upload_dir = "data/temp_uploads"
                
                # Reset counts for batch runs
                st.session_state["processed_count"] = len(uploaded_files)
                st.session_state["total_scores"] = []
                st.session_state["parsed_skills"] = []

                for idx, uploaded_file in enumerate(uploaded_files):
                    try:
                        # Step A: Save file
                        saved_path = file_handler.save_uploaded_file(uploaded_file, upload_dir)
                        
                        # Step B: Text Preview Feature
                        if uploaded_file.type == "text/plain":
                            file_content = uploaded_file.getvalue().decode("utf-8")
                            with st.expander(f"👀 Preview Raw Text: {uploaded_file.name}"):
                                st.text(file_content[:1000])
                        
                        # Step C: Parse Resume
                        parsed_data = resume_parser.parse_resume(saved_path)
                        st.session_state["latest_parsed_data"] = parsed_data

                        # Step D: JSON Output View
                        st.markdown(f"### 📄 {uploaded_file.name}")
                        st.json(parsed_data)
                        
                        # Extract skills and experience level
                        candidate_skills = parsed_data.get("skills", [])
                        skills_found = len(candidate_skills)
                        candidate_level = parsed_data.get("candidate_level", "Beginner")

                        # Collect parsed skills in session state
                        for s in candidate_skills:
                            if s.lower() not in st.session_state["parsed_skills"]:
                                st.session_state["parsed_skills"].append(s.lower())

                        # Step E: Calculate Score
                        total_score = (
                            candidate_scorer.calculate_total_score(skills_found, candidate_level) 
                            if skills_found > 0 else 0
                        )
                        st.session_state["total_scores"].append(total_score)

                        # Step F: Dynamic Metric Cards
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.metric(
                                label="⚡ Extraction Precision", 
                                value=f"{skills_found} Skills Found",
                                delta="Structural Match" if skills_found > 0 else "No Skills Detected"
                            )
                        with col_b:
                            st.metric(
                                label="🏆 Candidate / Employability Score", 
                                value=f"{total_score} pts",
                                delta=f"Level: {candidate_level}"
                            )
                        
                        st.markdown("---")
                        
                        # Step G: Skill Recommendation
                        st.markdown("### 🎯 Skill Recommendations")
                        
                        target_role = st.selectbox(
                            "Select Target Role for Gap Analysis:",
                            ["ML Engineer", "Data Scientist", "Data Engineer", "Software Engineer"],
                            key=f"target_role_{uploaded_file.name}_{idx}"
                        )
                        
                        rec_result = skill_engine.recommend_skills(candidate_skills, target_role)
                        
                        if isinstance(rec_result, dict):
                            missing_skills = rec_result.get("missing_skills", rec_result.get("missing", []))
                        else:
                            missing_skills = rec_result
                        
                        if missing_skills:
                            st.warning(f"**Recommended Skills to Learn for {target_role}:**")
                            for skill in missing_skills:
                                st.markdown(f"- 🔹 **{str(skill).title()}**")
                        else:
                            st.success(f"🎉 Great match! Candidate already possesses all key skills for **{target_role}**.")
                            
                        st.markdown("---")
                        
                    except Exception as error:
                        st.error(f"Error processing {uploaded_file.name}: {str(error)}")
                        
                st.success("Pipeline processing complete!")
    else:
        st.info("💡 Pro-Tip: Drag multiple resume profiles simultaneously to batch-score your pool.")

# ---------------------------------------------------------
# TAB 2: Interview Questions Only (Report Generator Integrated)
# ---------------------------------------------------------
with tab2:
    st.markdown("### 🎯 Technical Interview Question Generator")
    
    # Check if we have parsed candidate data from tab1 to generate full report
    if st.session_state["latest_parsed_data"]:
        interview_report = report_generator.generate_report(st.session_state["latest_parsed_data"])
        
        st.markdown("### 🎯 Generated Interview Preparation Report")
        
        questions_dict = interview_report.get("interview_questions", {})
        if questions_dict:
            for skill, questions in questions_dict.items():
                st.markdown(f"#### 💻 {skill.title()}")
                for number, question in enumerate(questions, start=1):
                    st.write(f"{number}. {question}")
        else:
            st.info("No specific skill questions found in the report.")
            
    else:
        # Fallback to interactive skill selector if no resume uploaded yet
        st.write("Generate technical interview questions based on selected candidate skills.")

        default_skill_pool = ["python", "sql", "machine learning", "java", "c++", "docker", "aws"]
        all_available_skills = list(set(default_skill_pool + st.session_state["parsed_skills"]))

        candidate_skills = st.multiselect(
            "Select candidate skills",
            options=all_available_skills,
            default=st.session_state["parsed_skills"] if st.session_state["parsed_skills"] else None
        )

        if candidate_skills:
            questions = question_generator.generate_questions_with_skills(candidate_skills)

            st.success(f"Questions generated for {len(candidate_skills)} skill(s).")

            for skill, skill_questions in questions.items():
                st.markdown(f"#### 💻 {skill.title()}")
                for number, question in enumerate(skill_questions, start=1):
                    st.write(f"{number}. {question}")
        else:
            st.info("Select candidate skills above or upload a resume in Tab 1 to generate interview questions.")

# ---------------------------------------------------------
# TAB 3: Project Overview
# ---------------------------------------------------------
with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🧩 Platform Architecture & Features")
    st.write("""
    This engineering platform orchestrates structural resume analysis, standardizes ambiguous applicant 
    datasets, ranks candidate experience thresholds programmatically, and automatically engineers analytical assets.
    """)
    
    st.markdown("#### Core Subsystems Running:")
    st.markdown("""
    *   **Automated Extraction Pipeline:** Validates schema consistency.
    *   **Feature-Engineering Weight Matrix:** Determines structural tiers (Beginner, Intermediate, Advanced).
    *   **Candidate Scoring Engine:** Calculates deterministic baseline applicant employability values.
    *   **Job Matching Engine:** Correlates profile token overlaps against variable vacancy targets.
    *   **Skill Recommendation Engine:** Identifies candidate skill gaps against industry target roles.
    """)
    st.markdown('</div>', unsafe_allow_html=True)