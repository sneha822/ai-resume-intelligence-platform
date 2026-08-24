# AI Resume Intelligence & Interview Copilot

An end-to-end resume intelligence platform that analyzes
candidate profiles against job descriptions, extracts
relevant skills, calculates compatibility scores, and
ranks candidates for a specific role.

## 🚀 Features

- Resume parsing
- Email and phone extraction
- Skill extraction
- Job description keyword extraction
- Resume ↔ JD token matching
- Similarity scoring
- Match-score calculation
- Match explanation
- Candidate ranking
- Batch candidate evaluation
- Error handling and logging
- Interactive Streamlit dashboard

## 🏗️ Architecture

Resume
  ↓
Resume Parser
  ↓
Skill Extraction
  ↓
Job Description Parser
  ↓
Keyword Matching
  ↓
Similarity Scoring
  ↓
Candidate Ranking
  ↓
Batch Evaluation
  ↓
Streamlit Dashboard

## 🛠️ Tech Stack

- Python
- Pandas
- SQLite
- Streamlit
- Scikit-learn
- Git & GitHub

## 📂 Project Structure

ai-resume-intelligence-platform/

├── app.py
├── config.py
├── requirements.txt
├── README.md
├── data/
├── src/
└── tests/

## ⚙️ Installation

Clone the repository:

git clone <your-repository-url>

Create an environment:

python -m venv .venv

Activate the environment.

Install dependencies:

pip install -r requirements.txt

## ▶️ Run the Application

streamlit run app.py

## 📊 Pipeline

1. Upload resumes
2. Parse candidate information
3. Upload/select a job description
4. Extract JD keywords
5. Match candidate skills
6. Calculate match scores
7. Rank candidates
8. Review candidate explanations

## 🧪 Testing

The project contains day-by-day testing scripts covering:

- Resume parsing
- Feature engineering
- Scoring
- JD parsing
- Matching
- Ranking
- Batch evaluation
- Error handling
- End-to-end integration

## 🎯 Project Goal

The goal of this project is to build an engineering-focused
resume intelligence system that demonstrates practical
application of data processing, NLP-style text matching,
scoring systems, backend logic, and interactive deployment.

## 👩‍💻 Author

Sneha Kumari

B.Tech — Electronics & Communication Engineering