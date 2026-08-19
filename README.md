# 📄 AI Resume Intelligence Platform & Interview Copilot

An end-to-end machine learning platform that parses resume files, extracts structured candidate features, stores applicant data, and utilizes Machine Learning to automatically classify candidate experience levels and roles while generating tailored interview paths.

---

## 🛠️ Features & Subsystems

*   ✅ **Resume Intake & Advanced Parsing:** Upload and parse raw `.pdf` (using `pdfplumber` and `PyPDF2`) and `.txt` resume files.
*   ✅ **Feature Extraction:** Extracts key numerical features including skill count, experience years, project count, and certifications.
*   ✅ **Candidate Database & Search:** Programmatic storage and candidate search functionality.
*   ✅ **Dataset & ML Pipeline:** Automated dataset generation, statistics calculation, train/test split, and trained Logistic Regression model for candidate classification.
*   ✅ **Interview Question Generator:** Rule-based technical question generation mapped directly from candidate skills.
*   ✅ **Interactive Streamlit Dashboard:** Multi-tab frontend UI for resume uploads, real-time metrics, live extraction visualization, and question generation.

---

## 🧠 Machine Learning Overview

*   **Model:** Logistic Regression (`scikit-learn`)
*   **Target:** Candidate Experience Level Classification (`candidate_level`)
*   **Input Features:** 
    *   `skill_count`
    *   `experience_years`
    *   `project_count`
    *   `certification_count`
*   **Model Serialization:** Serialized artifact saved to `models/role_classifier.pkl` via `joblib`.

---

## 📂 Project Structure

```text
ai-resume-platform/
│
├── app/
│   └── app.py                            # Streamlit Frontend UI
│
├── src/
│   ├── parser.py                         # Resume parsing engine (PyPDF2 & pdfplumber)
│   ├── feature_extractor.py              # Numerical feature extraction
│   ├── dataset_builder.py                # Formats candidate dataset
│   ├── dataset_statistics.py             # Dynamic dataset metrics calculation
│   ├── data_splitter.py                  # Train/Test splitting utility
│   ├── database.py                       # Storage handler
│   ├── search.py                         # Candidate search logic
│   ├── model_trainer.py                  # Logistic Regression trainer
│   └── interview_question_generator.py   # Skill-to-question generator module
│
├── models/
│   └── role_classifier.pkl               # Serialized trained ML model
│
├── data/
│   ├── temp_uploads/                     # Staging directory for uploaded files
│   ├── processed_candidates.csv
│   ├── train_candidates.csv
│   └── test_candidates.csv
│
├── requirements.txt                      # Project dependencies
└── README.md                             # Platform documentation