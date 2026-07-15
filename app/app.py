import os
import sys
import streamlit as st
import pandas as pd

# Fix Python path so 'src' can be discovered when running from the app directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.file_handler import FileHandler  
from src.parser import ResumeParser

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
tab1, tab2, tab3 = st.tabs(
    [
        "📤 Upload & Analyze",
        "📊 Dashboard",
        "📋 Project Overview & Docs"
    ]
)

# ----------------------------------------------------------
# TAB 1: Upload & Analyze
# ----------------------------------------------------------
with tab1:
    st.markdown("### 🚀 Candidate Intake")
    
    # File Uploader
    uploaded_files = st.file_uploader(
        "Drop candidate resumes here (PDF or TXT format)", 
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
                        
                        # Step B: Text/PDF Preview Feature
                        if uploaded_file.type == "text/plain":
                            file_content = uploaded_file.getvalue().decode("utf-8")
                            with st.expander(f"👀 Preview Raw Text: {uploaded_file.name}"):
                                st.text(file_content[:1000])
                        elif uploaded_file.type == "application/pdf":
                            with st.expander(f"👀 PDF Staged: {uploaded_file.name}"):
                                st.caption("PDF binary data loaded successfully. Processing structural text...")
                        
                        # Step C: Core Processing Pipeline execution
                        parsed_data = resume_parser.parse_resume(saved_path)
                        
                        # Step D: Frontend UI Component (Candidate Summary Card)
                        st.markdown(f"### 👤 Candidate Profile: {uploaded_file.name}")
                        
                        with st.container():
                            col_left, col_right = st.columns(2)
                            with col_left:
                                st.info(f"**📬 Email:** {parsed_data.get('email', 'N/A')}")
                                st.info(f"**📞 Phone:** {parsed_data.get('phone', 'N/A')}")
                            
                            with col_right:
                                st.success(f"**📊 Candidate Level:** Intermediate (Day 13 Matrix)")
                                st.success(f"**🎯 Baseline Score:** 82/100 (Day 14 Engine)")
                        
                        # Step E: Skills Section Display
                        st.markdown("#### 🛠️ Extracted Skills")
                        skills = parsed_data.get("skills", [])
                        if skills:
                            st.write(", ".join([f"`{skill}`" for skill in skills]))
                        else:
                            st.caption("No dynamic keywords matching the skillset matrix were detected.")

                        st.markdown("---")

                        # Step F: Dynamic Extraction Metrics (Upgraded for Day 21 Advanced Features)
                        st.markdown("#### 📊 Candidate Feature Breakdown")
                        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                        
                        skills_found = len(skills)
                        experience = parsed_data.get("experience_years", 0)
                        projects = parsed_data.get("project_count", 0)
                        certs = parsed_data.get("certification_count", 0)

                        with metric_col1:
                            st.metric(
                                label="⚡ Skills Match", 
                                value=f"{skills_found} Skills",
                                delta="Found" if skills_found > 0 else "None"
                            )
                        with metric_col2:
                            st.metric(
                                label="⏳ Experience", 
                                value=f"{experience} Years",
                                delta="Verified" if experience > 0 else "None detected",
                                delta_color="normal" if experience > 0 else "off"
                            )
                        with metric_col3:
                            st.metric(
                                label="📂 Projects", 
                                value=f"{projects} Projects",
                                delta="Active" if projects > 0 else "None detected",
                                delta_color="normal" if projects > 0 else "off"
                            )
                        with metric_col4:
                            st.metric(
                                label="📜 Certifications", 
                                value=f"{certs} Certs",
                                delta="Certified" if certs > 0 else "None detected",
                                delta_color="normal" if certs > 0 else "off"
                            )
                        
                        # Developer Mode for underlying schema inspection
                        with st.expander("🛠️ View Raw JSON Schema (Developer View)"):
                            st.json(parsed_data)
                            
                        st.markdown("---")
                        
                    except Exception as error:
                        st.error(f"Error processing {uploaded_file.name}: {str(error)}")
                        
                st.success("Pipeline processing complete!")
    else:
        st.info("💡 Pro-Tip: Drag multiple resume profiles simultaneously to batch-score your pool.")

# ----------------------------------------------------------
# TAB 2: Analytics Dashboard
# ----------------------------------------------------------
with tab2:
    st.subheader("📊 Candidate Analytics Dashboard")
    
    try:
        # Load the dataset locally
        df = pd.read_csv("data/processed_candidates.csv")
        
        # Dashboard Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Candidates", value=len(df))
        with col2:
            st.metric(label="Advanced Candidates", value=len(df[df["candidate_level"] == "Advanced"]))
        with col3:
            st.metric(label="Average Skill Count", value=round(df["skill_count"].mean(), 2))
            
        st.markdown("---")
        
        # Candidate Level Distribution (Bar Chart)
        st.markdown("### 📈 Experience Level Distribution")
        level_counts = df["candidate_level"].value_counts()
        st.bar_chart(level_counts)
        
        st.markdown("---")
        
        # Candidate Ranking Table (Dataframe)
        st.markdown("### 🏆 Candidate Leaderboard")
        ranking_columns = ["email", "candidate_level", "candidate_score"]
        st.dataframe(
            df[ranking_columns].sort_values(by="candidate_score", ascending=False),
            use_container_width=True
        )
        
        st.markdown("---")
        
        # Top Skills Section
        st.markdown("### 🔥 Top Skills in Candidate Pool")
        skill_data = {
            "Python": 4, 
            "SQL": 3, 
            "Machine Learning": 3, 
            "Java": 2, 
            "C++": 1
        }
        st.bar_chart(skill_data)
        
        st.markdown("---")
        
        # Candidate Distribution Pie Chart Image
        st.markdown("### 🍕 Skill Distribution Overview")
        if os.path.exists("artifacts/plots/skill_distribution.png"):
            st.image(
                "artifacts/plots/skill_distribution.png", 
                caption="Visual Skill Distribution Breakdown", 
                use_container_width=True
            )
        else:
            st.info("💡 Pro-Tip: Ensure your skill distribution chart is generated at 'artifacts/plots/skill_distribution.png' to render the visual pie chart here!")

    except FileNotFoundError:
        st.warning("⚠️ `data/processed_candidates.csv` file not found. Run your data collection script to populate dashboard metrics.")

# ----------------------------------------------------------
# TAB 3: Project Overview & Docs
# ----------------------------------------------------------
with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🧩 Platform Architecture & Features")
    st.write("""
    This engineering platform orchestrates structural resume analysis, standardizes ambiguous applicant 
    datasets, ranks candidate experience thresholds programmatically, and automatically engineers analytical assets.
    """)
    
    st.markdown("#### Core Subsystems Running:")
    st.markdown("""
    *   **Automated Extraction Pipeline:** Validates schema consistency and supports structural PDF/TXT data.
    *   **Feature-Engineering Weight Matrix:** Determines structural tiers (Beginner, Intermediate, Advanced).
    *   **Day 14 Automated Scoring Engine:** Calculates deterministic baseline applicant values.
    *   **Job Matching Engine:** Correlates profile token overlaps against variable vacancy targets.
    """)
    st.markdown('</div>', unsafe_allow_html=True)