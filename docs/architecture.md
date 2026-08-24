# System Architecture

## Overview

The AI Resume Intelligence Platform follows a modular
pipeline architecture.

## Processing Flow

1. Resume upload
2. File storage
3. Resume parsing
4. Candidate data extraction
5. Job description parsing
6. Keyword matching
7. Similarity calculation
8. Match scoring
9. Candidate ranking
10. Batch evaluation
11. Dashboard visualization

## Modules

### File Handler

Responsible for storing uploaded resume files.

### Resume Parser

Coordinates text reading, cleaning, and skill extraction.

### Job Description Parser

Extracts relevant terms from job descriptions.

### Job Matcher

Compares candidate skills against job requirements.

### Match Scorer

Calculates compatibility metrics.

### Batch Evaluator

Processes multiple candidates and generates a ranked
candidate dataset.

### Streamlit Application

Provides the user-facing interface.

## Design Principle

The application separates presentation logic from
business logic.

Streamlit handles the interface while processing,
matching, scoring, and ranking remain inside the `src`
package.