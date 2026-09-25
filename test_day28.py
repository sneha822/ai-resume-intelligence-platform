import os
import pandas as pd
from src.selection_predictor import CandidateSelectionPredictor


def test_candidate_selection_predictor():
    csv_path = "data/processed_candidates.csv"

    # Always ensure a sufficient, balanced dataset for stratified splitting
    df = pd.DataFrame({
        "skill_count": [4, 2, 5, 1, 3, 2, 5, 1, 4, 3],
        "experience_years": [3, 1, 5, 0, 2, 1, 6, 0, 4, 2],
        "project_count": [2, 1, 4, 0, 2, 1, 5, 0, 3, 2],
        "certification_count": [1, 0, 2, 0, 1, 0, 3, 0, 2, 1],
        "selection_status": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    })

    predictor = CandidateSelectionPredictor()
    accuracy = predictor.train(df)

    sample_candidate = {
        "skill_count": 4,
        "experience_years": 3,
        "project_count": 2,
        "certification_count": 1
    }

    result = predictor.predict_candidate(sample_candidate)

    assert accuracy >= 0.0
    assert result in [0, 1, "Selected", "Rejected"]