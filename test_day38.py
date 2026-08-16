import pandas as pd

from src.pca_visualizer import (
    CandidatePCAVisualizer
)


# Load the dataset generated on Day 37
dataframe = pd.read_csv(
    "data/processed_candidates.csv"
)


# Initialize PCA visualizer
visualizer = CandidatePCAVisualizer()


# Reduce candidate features
dataframe = visualizer.transform(
    dataframe
)


print(
    "=== PCA TRANSFORMATION ==="
)

print(
    dataframe[
        [
            "email",
            "cluster",
            "cluster_level",
            "PC1",
            "PC2"
        ]
    ]
)


# Save PCA-enhanced dataset
dataframe.to_csv(
    "data/processed_candidates.csv",
    index=False
)


# Generate visualization
visualizer.plot_clusters(
    dataframe,
    "artifacts/candidate_clusters_pca.png"
)


print(
    "\nPCA visualization saved successfully."
)

print(
    "Saved to: artifacts/candidate_clusters_pca.png"
)