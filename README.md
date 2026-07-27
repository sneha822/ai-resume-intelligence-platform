# 📄 AI Resume Intelligence Platform

A modular, data-driven platform designed to ingest unstructured resumes (PDF/TXT), extract key candidate properties, compute numerical feature metrics, and prepare ML-ready datasets for applicant tracking and candidate ranking.

---

## 📌 Project Overview

The **AI Resume Intelligence Platform** automates the labor-intensive process of parsing applicant profiles. By converting unstructured resume documents into structured tabular data, the platform enables seamless feature engineering, candidate scoring, and instant skill-based searching—laying the foundation for predictive machine learning models.

---

## 🏗️ Folder Structure

```text
ai-resume-intelligence-platform/
│
├── app/
│   └── app.py                      # Interactive Streamlit Web Dashboard
│
├── src/
│   ├── file_handler.py             # File saving & stream buffer handling
│   ├── parser.py                   # Resume parsing & token extraction
│   ├── dataset_builder.py          # Numerical feature matrix generator
│   ├── dataset_statistics.py       # Statistical summary generator
│   ├── data_splitter.py           # Train/Test dataset splitter module
│   └── data_summary.py             # Dataset schema & info utility
│
├── data/
│   ├── temp_uploads/               # Staging area for uploaded resume files
│   ├── processed_candidates.csv    # Consolidated candidate master dataset
│   ├── train_candidates.csv        # ML training subset
│   └── test_candidates.csv         # ML testing evaluation subset
│
├── test_pipeline_flow.py           # End-to-end feature pipeline test suite
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation