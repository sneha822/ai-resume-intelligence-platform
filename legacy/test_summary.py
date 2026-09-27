import pandas as pd

from src.data_summary import DatasetSummary

df = pd.read_csv(
    "data/train_candidates.csv"
)

summary = DatasetSummary()

summary.dataset_information(df)