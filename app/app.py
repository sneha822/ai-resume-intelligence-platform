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
                        
                        # Step D: Frontend UI Component (Candidate Summary Card)
                        st.markdown(f"### 👤 Candidate Profile: {uploaded_file.name}")
                        
                        with st.container():
                            col_left, col_right = st.columns(2)
                            with col_left:
                                st.write(f"**📬 Email:** {parsed_data.get('email', 'N/A')}")
                                st.write(f"**📞 Phone:** {parsed_data.get('phone', 'N/A')}")
                            
                            with col_right:
                                # Placeholders referencing your Day 13 Matrix & Day 14 Scoring Engine logic
                                st.write(f"**📊 Candidate Level:** Intermediate (Day 13 Matrix)")
                                st.write(f"**🎯 Baseline Score:** 82/100 (Day 14 Engine)")
                        
                        # Step E: Dynamic Extraction Metrics
                        skills_found = len(parsed_data.get("skills", []))
                        st.metric(
                            label="⚡ Skills Extracted", 
                            value=f"{skills_found}",
                            delta="Structural Match" if skills_found > 0 else "No Skills Detected"
                        )
                        
                        # Optional: Keep raw output in an expander for debugging purposes
                        with st.expander("🛠️ View Raw JSON Schema"):
                            st.json(parsed_data)
                            
                        st.markdown("---")
                        
                    except Exception as error:
                        st.error(f"Error processing {uploaded_file.name}: {str(error)}")
                        
                st.success("Pipeline processing complete!")
    else:
        st.info("💡 Pro-Tip: Drag multiple resume profiles simultaneously to batch-score your pool.")

with tab2:
    st.subheader("📊 Candidate Analytics Dashboard")
    
    # Step 2: Load the dataset locally
    df = pd.read_csv("data/processed_candidates.csv")
    
    # Step 3: Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Candidates", value=len(df))
    with col2:
        st.metric(label="Advanced Candidates", value=len(df[df["candidate_level"] == "Advanced"]))
    with col3:
        st.metric(label="Average Skill Count", value=round(df["skill_count"].mean(), 2))
        
    st.markdown("---")
    
    # Step 4: Candidate Level Distribution (Bar Chart)
    st.markdown("### 📈 Experience Level Distribution")
    level_counts = df["candidate_level"].value_counts()
    st.bar_chart(level_counts)
    
    st.markdown("---")
    
    # Step 5: Candidate Ranking Table (Dataframe)
    st.markdown("### 🏆 Candidate Leaderboard")
    ranking_columns = ["email", "candidate_level", "candidate_score"]
    st.dataframe(
        df[ranking_columns].sort_values(by="candidate_score", ascending=False),
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Step 6: Top Skills Section
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
    
    # Step 7: Candidate Distribution Pie Chart
    st.markdown("### 🍕 Skill Distribution Overview")
    try:
        st.image(
            "artifacts/plots/skill_distribution.png", 
            caption="Visual Skill Distribution Breakdown", 
            use_container_width=True
        )
    except Exception:
        st.info("💡 Pro-Tip: Ensure your skill distribution chart is generated at 'artifacts/plots/skill_distribution.png' to render the visual pie chart here!")

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
    """)
    st.markdown('</div>', unsafe_allow_html=True)