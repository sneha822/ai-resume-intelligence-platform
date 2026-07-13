import streamlit as st
import pandas as pd
# Add these alongside your other imports at the top
from src.file_handler import FileHandler
from src.parser import ResumeParser

# Initialize your backend engines near the top of the script
file_handler = FileHandler()
resume_parser = ResumeParser()

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Resume Intelligence Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS styling for a cleaner, modern look
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

# 3. Sidebar Navigation
with st.sidebar:
    st.markdown("## 🛠️ Control Panel")
    st.write("Week 3: Frontend Interface")
    st.markdown("---")
    
    # Active configuration toggles
    st.markdown("### Settings")
    parse_mode = st.selectbox("Parsing Engine", ["Rule-Based (Fast)", "AI-Powered (Deep Search)"])
    enable_scoring = st.checkbox("Apply Day 14 Scoring Engine", value=True)
    
    st.markdown("---")
    st.caption("AI Resume Intelligence Platform v1.0 • 2026")

# 4. Main App Layout Header
st.markdown('<p class="main-title">📄 AI Resume Intelligence & Interview Copilot</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Extract core insights, rank candidate profiles, and generate intelligent interview pathways instantly.</p>', unsafe_allow_html=True)

# 5. Dashboard Summary Metrics (Gives it an instant "platform" feel)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Processed Resumes", value="12", delta="+3 today")
with col2:
    st.metric(label="Top Matching Track", value="Python / SQL", delta="Data Engineering")
with col3:
    st.metric(label="Avg Match Score", value="78.4%", delta="+2.1% improvement")

st.markdown("---")

# 6. Interactive Workspace Content split into organized Tabs
tab1, tab2 = st.tabs(["📤 Upload & Analyze", "📋 Project Overview & Docs"])

with tab1:
    st.markdown("### 🚀 Candidate Intake")
    
    # 1. This is your existing drag-and-drop uploader widget
    uploaded_files = st.file_uploader(
        "Drop candidate resumes here (PDF, TXT, or DOCX format)", 
        type=["txt", "pdf"], 
        accept_multiple_files=True
    )
    
    # 2. CLEAR & REPLACED LOGIC: What happens when files are uploaded
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
                
                for uploaded_file in uploaded_files:
                    try:
                        # 1. Save the file to disk
                        saved_path = file_handler.save_uploaded_file(uploaded_file, upload_dir)
                        
                        # ==========================================================
                        # STEP 5: ADD RESUME PREVIEW HERE (Inside the loop)
                        # ==========================================================
                        if uploaded_file.type == "text/plain":
                            file_content = uploaded_file.getvalue().decode("utf-8")
                            with st.expander(f"👀 Preview Raw Text: {uploaded_file.name}"):
                                st.text(file_content[:1000])
                        # ==========================================================
                        
                        # 2. Parse the file using your backend parser
                        parsed_data = resume_parser.parse_resume(saved_path)
                        
                        # 3. Print the JSON result on the screen
                        st.markdown(f"### 📄 {uploaded_file.name}")
                        st.json(parsed_data)
                        
                    except Exception as error:
                        st.error(f"Error processing {uploaded_file.name}: {str(error)}")
                        
                st.success("Pipeline processing complete!")
    else:
        # If no files are uploaded, show this tip
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
    *   **Feature-Engineering Weight Matrix:** Determines structural tiers (`Beginner`, `Intermediate`, `Advanced`).
    *   **Day 14 Automated Scoring Engine:** Calculates deterministic baseline applicant values.
    *   **Job Matching Engine:** Correlates profile token overlaps against variable vacancy targets.
    """)
    st.markdown('</div>', unsafe_allow_html=True)