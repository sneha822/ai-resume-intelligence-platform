# V2 Architecture

## Overview

V2 extends the deterministic V1 resume intelligence system
with an AI reasoning layer.

## Data Flow

Resume
→ Hybrid Parser
→ CandidateProfile
→ Candidate Knowledge Base
→ Semantic Evaluation
→ Evidence
→ Natural Language Search
→ Recruiter Copilot

## Component Responsibilities

### Hybrid Parser

Responsible for combining AI-based structured extraction
with the original deterministic parser.

### Candidate Evaluator

Responsible for semantic job-fit analysis.

### Knowledge Base

Responsible for candidate storage and deterministic retrieval.

### Candidate Search

Responsible for converting natural-language recruiter
requests into structured filters.

### Recruiter Copilot

Responsible for conversational interaction over candidate
context.

## Design Principles

1. Modular components
2. Provider abstraction
3. Deterministic fallback
4. Evidence-based reasoning
5. Testability
6. Separation of concerns
7. Backward compatibility with V1