import pandas as pd
from src.feature_engineering import FeatureEngineer

# Step 1: Load the dataset you built on Day 12
df = pd.read_csv("data/processed_candidates.csv")

# Step 2: Initialize your new Feature Engineer
engineer = FeatureEngineer()

# Step 3: Run your new data transformations
df = engineer.skill_count(df)
df = engineer.candidate_level(df)

# Step 4: Save the newly engineered dataset back to CSV
df.to_csv("data/processed_candidates.csv", index=False)

# Step 5: Print the results to your terminal to verify!
print("--- Processed Dataset Preview ---")
print(df)
print("\nDataset successfully updated and saved!")