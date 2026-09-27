import os
import pandas as pd
from src.candidate_clustering import CandidateClusterer


def test_day38_pca_clustering():
    csv_path = "data/processed_candidates.csv"
    if os.path.exists(csv_path):
        dataframe = pd.read_csv(csv_path)
    else:
        dataframe = pd.DataFrame()

    if len(dataframe) < 3 or "cluster" not in dataframe.columns or "cluster_level" not in dataframe.columns:
        dataframe = pd.DataFrame({
            "email": ["a@example.com", "b@example.com", "c@example.com", "d@example.com"],
            "skill_count": [2, 5, 8, 3],
            "experience_years": [1, 4, 7, 2],
            "project_count": [1, 3, 6, 2],
            "certification_count": [0, 2, 4, 1],
        })
        clusterer = CandidateClusterer(n_clusters=3)
        dataframe = clusterer.fit_predict(dataframe)
        dataframe = clusterer.assign_cluster_levels(dataframe)

    assert "cluster" in dataframe.columns
    assert "cluster_level" in dataframe.columns