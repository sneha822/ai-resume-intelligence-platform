import os
import pandas as pd
from src.model_comparison import ModelComparator


def test_day29_model_comparison():
    df = pd.DataFrame({
        "skill_count": [2, 5, 8, 3, 6, 1, 2, 5, 8, 3, 6, 1],
        "experience_years": [1, 4, 7, 2, 5, 0, 1, 4, 7, 2, 5, 0],
        "project_count": [1, 3, 6, 2, 4, 0, 1, 3, 6, 2, 4, 0],
        "certification_count": [0, 2, 4, 1, 3, 0, 0, 2, 4, 1, 3, 0],
        "candidate_level": [
            "Beginner", "Intermediate", "Advanced",
            "Beginner", "Advanced", "Intermediate",
            "Beginner", "Intermediate", "Advanced",
            "Beginner", "Advanced", "Intermediate"
        ]
    })

    comparator = ModelComparator()
    results = comparator.compare_models(df)
    assert results is not None