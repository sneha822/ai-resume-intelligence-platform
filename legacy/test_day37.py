import os
import pandas as pd
from src.candidate_clustering import CandidateClusterer


def test_candidate_clustering():
    csv_path = "data/processed_candidates.csv"

    # 1. Load data or construct dummy dataset with enough rows for 3 clusters
    if os.path.exists(csv_path):
        dataframe = pd.read_csv(csv_path)
    else:
        dataframe = pd.DataFrame()

    # Ensure dataset has at least 3 samples (n_samples >= n_clusters)
    if len(dataframe) < 3:
        dataframe = pd.DataFrame({
            "email": ["a@example.com", "b@example.com", "c@example.com", "d@example.com"],
            "skill_count": [2, 5, 8, 3],
            "experience_years": [1, 4, 7, 2],
            "project_count": [1, 3, 6, 2],
            "certification_count": [0, 2, 4, 1],
        })

    # 2. Create clustering model
    clusterer = CandidateClusterer(n_clusters=3)

    # 3. Assign clusters
    dataframe = clusterer.fit_predict(dataframe)

    # 4. Assign cluster levels (Beginner, Intermediate, Advanced)
    dataframe = clusterer.assign_cluster_levels(dataframe)

    print("\n=== CANDIDATE CLUSTERS ===")
    print(
        dataframe[
            [
                "email",
                "skill_count",
                "experience_years",
                "project_count",
                "certification_count",
                "cluster",
            ]
        ]
    )

    # 5. Display cluster summary
    summary = clusterer.get_cluster_summary(dataframe)
    print("\n=== CLUSTER SUMMARY ===")
    print(summary)

    # 6. Display mapped cluster levels
    print("\n=== CLUSTER LEVELS ===")
    print(dataframe[["email", "cluster", "cluster_level"]])

    # Assertions for pytest
    assert "cluster" in dataframe.columns
    assert "cluster_level" in dataframe.columns
    assert len(dataframe["cluster"].unique()) <= 3