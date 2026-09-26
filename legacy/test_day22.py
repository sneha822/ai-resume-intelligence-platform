import pandas as pd

from src.dataset_builder import (
    CandidateDatasetBuilder
)

df = pd.read_csv(
    "data/processed_candidates.csv"
)

builder = CandidateDatasetBuilder()

df = builder.add_numerical_features(
    df
)

df.to_csv(
    "data/processed_candidates.csv",
    index=False
)

print(df.head())