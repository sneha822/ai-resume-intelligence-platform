import pandas as pd
from src.eda import CandidateEDA

# 1. Load the fixed dataset
df = pd.read_csv("data/processed_candidates.csv")

# 2. Initialize the EDA module
eda = CandidateEDA()

# 3. Print Results
print("=== COMPLETE EDA RUN ===")
print(f"Total Profiles Processed : {eda.total_candidates(df)}")
print(f"Unique Email Signatures  : {eda.unique_emails(df)}")
print("\n--- Missing Values Per Column ---")
print(eda.missing_values(df))

print("\n--- Candidate Level Distribution ---")
print(eda.level_distribution(df))