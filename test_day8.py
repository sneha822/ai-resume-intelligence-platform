from src.data_cleaner import (
    CandidateDataCleaner
)

cleaner = CandidateDataCleaner()

df = cleaner.load_data(
    "data/candidates.csv"
)

cleaned_df = cleaner.clean_dataset(df)

cleaned_df.to_csv(
    "data/processed_candidates.csv",
    index=False
)

print(cleaned_df.head())