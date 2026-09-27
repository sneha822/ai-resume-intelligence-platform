```markdown
# Week 1 Module Architecture & Workflow

This document logs the responsibilities of the backend modules built during the Week 1 foundation sprint.

### 1. `reader.py`
Reads raw string arrays out of localized text files located in the `data/raw/` directory.

### 2. `preprocessing.py`
Cleans input text by removing excessive white spaces and normalizing case variants.

### 3. `extraction.py`
Uses structured Regular Expressions to accurately detect emails, phone layouts, and technical toolsets.

### 4. `parser.py`
The master coordinator. Pulls data via the reader, cleans it using preprocessing, extracts target parameters, and fits it into a clean profile.

### 5. `candidate_profile.py`
Defines the standard data template (blueprint) for how a candidate's profile is formatted in memory.

### 6. `storage.py`
Accepts list records, converts them into a Pandas DataFrame matrix, and writes them out cleanly to `data/candidates.csv`.

### 7. `validation.py`
Acts as a security checkpoint, verifying that emails are present and skills belong to a pre-approved list before saving.

### 8. `logger.py`
Initializes system logging so application behaviors and unexpected bugs track cleanly inside `logs/project.log`.