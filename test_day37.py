import pandas as pd

from src.candidate_clustering import CandidateClusterer


# Load candidate dataset
dataframe = pd.read_csv("data/processed_candidates.csv")


# Create clustering model
clusterer = CandidateClusterer(n_clusters=3)


# Assign clusters
dataframe = clusterer.fit_predict(dataframe)


# Assign cluster levels (Beginner, Intermediate, Advanced)
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


# Display cluster characteristics
summary = clusterer.get_cluster_summary(dataframe)

print("\n=== CLUSTER SUMMARY ===")
print(summary)


# Display mapped cluster levels
print("\n=== CLUSTER LEVELS ===")
print(dataframe[["email", "cluster", "cluster_level"]])

dataframe.to_csv(
    "data/processed_candidates.csv",
    index=False
)