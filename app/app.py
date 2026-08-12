import os
import sys
import streamlit as st

# Fix Python path so 'src' modules can be imported when running from the app directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.file_handler import FileHandler  
from src.parser import ResumeParser  
from src.skill_recommender import SkillRecommendationEngine  # Check file name in src/ (e.g., skill_recommender)

# ==========================================================
# 1. Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Resume Intelligence Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# 3. Component Initialization
# ==========================================================
file_handler = FileHandler()
resume_parser = ResumeParser()
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
# 5. Header Layout
# ==========================================================
st.markdown('<p class="main-title">📄 AI Resume Intelligence & Interview Copilot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Extract core insights, rank candidate profiles, and generate intelligent interview pathways instantly.</p>', unsafe_allow_html=True)

# Dashboard Summary Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Processed Resumes", value="0", delta="Staging Empty")
with col2:
    st.metric(label="Top Matching Track", value="Python / SQL", delta="Data Engineering")
with col3:
    st.metric(label="Avg Match Score", value="N/A", delta="No data processed")

st.markdown("---")

# ==========================================================
# 6. Interactive Workspace (Tabs)
# ==========================================================
tab1, tab2 = st.tabs(["📤 Upload & Analyze", "📋 Project Overview & Docs"])

with tab1:
    st.markdown("### 🚀 Candidate Intake")
    
    # File Uploader
    uploaded_files = st.file_uploader(
        "Drop candidate resumes here (PDF, TXT, or DOCX format)", 
        type=["txt", "pdf"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.success(f"Successfully staged {len(uploaded_files)} file(s) for parsing!")
        
        # Pipeline Action Trigger
        if st.button("🔥 Run Intelligence Pipeline"):
            with st.spinner("Executing structural extraction and scoring algorithms..."):
                upload_dir = "data/temp_uploads"
                
                for uploaded_file in uploaded_files:
                    try:
                        # Step A: Save memory-buffered file to local disk
                        saved_path = file_handler.save_uploaded_file(uploaded_file, upload_dir)
                        
                        # Step B: Text Preview Feature
                        if uploaded_file.type == "text/plain":
                            file_content = uploaded_file.getvalue().decode("utf-8")
                            with st.expander(f"👀 Preview Raw Text: {uploaded_file.name}"):
                                st.text(file_content[:1000])
                        
                        # Step C: Core Processing Pipeline execution
                        parsed_data = resume_parser.parse_resume(saved_path)
                        
                        # Step D: Dynamic JSON Output View
                        st.markdown(f"### 📄 {uploaded_file.name}")
                        st.json(parsed_data)
                        
                        # Step E: Dynamic Extraction Metrics
                        skills_found = len(parsed_data.get("skills", []))
                        st.metric(
                            label="⚡ Extraction Precision", 
                            value=f"{skills_found} Skills Found",
                            delta="Structural Match" if skills_found > 0 else "No Skills Detected"
                        )
                        
                        st.markdown("---")
                        
                        # ==========================================================
                        # STEP 6: Skill Recommendation Section
                        # ==========================================================
                        st.markdown("### 🎯 Skill Recommendations")
                        
                        target_role = st.selectbox(
                            "Select Target Role for Gap Analysis:",
                            ["ML Engineer", "Data Scientist", "Data Engineer", "Software Engineer"],
                            key=f"target_role_{uploaded_file.name}"
                        )
                        
                        candidate_skills = parsed_data.get("skills", [])
                        
                        # Call recommendation engine
                        rec_result = skill_engine.recommend_skills(candidate_skills, target_role)
                        
                        # Extract list whether the return type is dict or list
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

with tab2:
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
    *   **Day 14 Automated Scoring Engine:** Calculates deterministic baseline applicant values.
    *   **Job Matching Engine:** Correlates profile token overlaps against variable vacancy targets.
    *   **Skill Recommendation Engine:** Identifies candidate skill gaps against industry target roles.
    """)
    st.markdown('</div>', unsafe_allow_html=True)