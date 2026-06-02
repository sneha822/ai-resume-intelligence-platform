# AI Resume Intelligence & Interview Copilot Platform

## 📌 Project Overview
The **AI Resume Intelligence & Interview Copilot Platform** is an end-to-end application designed to automate unstructured resume ingestion, parse core candidate features (emails, phone numbers, skills), validate profiles, and aggregate structured datasets using Pandas.

This project is built incrementally following industry-standard software engineering practices, including modular code structure, centralized logging, and strict data validation rules.

---

## 🛠️ Tech Stack
* **Language:** Python 3.13+
* **Data Handling:** Pandas
* **Text Processing:** Regular Expressions (Regex)
* **Version Control:** Git & GitHub

---

## 🚀 Current Features (Week 1 Foundation)
### 1. Resume Parsing & Processing
* **Text Extraction:** Ingests raw text files from local directories.
* **Text Cleaning:** Standardizes spacing and casing to prepare text for extraction.
* **Information Extraction:** Employs precise regular expressions to extract emails, phone numbers, and technical skills.

### 2. Data Management & Validation
* **Object-Oriented Profiling:** Models candidate data consistently in runtime memory.
* **Pandas Dataset Storage:** Converts candidate lists into clean 2D dataframes and saves them directly to `data/candidates.csv`.
* **Data Validation Gateway:** Checks profiles to ensure emails are valid and skills match our accepted baseline.

### 3. Application Telemetry
* **Centralized Logger:** Records all file adjustments and pipeline failures into `logs/project.log` instead of cluttering the console with `print` statements.

---

## 📂 Project Structure
```text
ai-resume-intelligence-platform/
├── data/                      # Persistent storage layers
│   ├── candidates.csv         # Structured dataset output
│   └── raw/                   # Unstructured candidate source files (.txt, .pdf)
├── logs/                      # System diagnostic logs
│   └── project.log
├── notes/                     # Architecture & sprint tracking notes
│   ├── week1_architecture.md
│   └── week1_review.md
├── src/                       # Core functional backend modules
│   ├── candidate_profile.py
│   ├── extraction.py
│   ├── helper.py
│   ├── logger.py
│   ├── parser.py
│   ├── preprocessing.py
│   ├── reader.py
│   ├── storage.py
│   ├── utils.py
│   └── validation.py
├── config.py                  # Global application configurations
├── README.md                  # Master repository overview
└── requirements.txt           # Explicit system dependencies