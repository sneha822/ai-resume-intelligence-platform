# 📄 AI Resume Intelligence Platform & Interview Copilot

An end-to-end machine learning platform that parses resume files, extracts structured candidate features, stores applicant data, and uses Machine Learning to automatically classify candidate experience levels and roles.

---

## 🛠️ Features & Progress

*   ✅ **Resume Intake & Parsing:** Upload and parse raw `.pdf` and `.txt` resume files.
*   ✅ **Feature Extraction:** Extracts key numerical features including skill count, experience years, project count, and certifications.
*   ✅ **Candidate Database:** Programmatic storage and candidate search functionality.
*   ✅ **Streamlit Dashboard:** Interactive UI with dynamic candidate metrics and live extraction pipelines.
*   ✅ **Dataset Pipeline:** Automated dataset generation, statistics, and train/test split functionality.
*   ✅ **Machine Learning Pipeline:** Trained Logistic Regression model for candidate classification and saved serialized artifacts.

---

## 🧠 Machine Learning Overview

*   **Model:** Logistic Regression (`scikit-learn`)
*   **Target:** Candidate Classification (`candidate_level`)
*   **Input Features:** 
    *   `skill_count`
    *   `experience_years`
    *   `project_count`
    *   `certification_count`
*   **Model Serialization:** Saved to `models/role_classifier.pkl` using `joblib`.

---

## 📂 Project Structure

```text
ai-resume-platform/
│
├── app/
│   └── app.py                     # Streamlit Frontend UI
│
├── src/
│   ├── parser.py                  # Resume parsing engine
│   ├── feature_extractor.py       # Numerical feature extraction
│   ├── dataset_builder.py         # Formats candidate dataset
│   ├── dataset_statistics.py      # Dynamic dataset metrics calculation
│   ├── data_splitter.py           # Train/Test splitting utility
│   ├── database.py                # Storage handler
│   ├── search.py                  # Candidate search logic
│   └── model_trainer.py           # Logistic Regression trainer
│
├── models/
│   └── role_classifier.pkl        # Serialized trained ML model
│
├── data/
│   ├── processed_candidates.csv
│   ├── train_candidates.csv
│   └── test_candidates.csv
│
├── test_day26.py                  # Pipeline and model training test script
└── README.md