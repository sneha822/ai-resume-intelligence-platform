import pandas as pd

from src.data_splitter import (
    CandidateDataSplitter
)

df = pd.read_csv(
    "data/processed_candidates.csv"
)

splitter = CandidateDataSplitter()

train_df, test_df = splitter.split_dataset(df)

train_df.to_csv(
    "data/train_candidates.csv",
    index=False
)

test_df.to_csv(
    "data/test_candidates.csv",
    index=False
)

print("Training Dataset")
print(train_df)

print("\nTesting Dataset")
print(test_df)