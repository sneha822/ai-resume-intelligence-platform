import pandas as pd

from src.dataset_statistics import (
    DatasetStatistics
)

df = pd.read_csv(
    "data/processed_candidates.csv"
)

stats = DatasetStatistics()

print(
    stats.numerical_summary(df)
)