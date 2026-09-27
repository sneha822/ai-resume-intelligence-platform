import pandas as pd
from src.feature_engineering import FeatureEngineer

# 1. Create a realistic multi-candidate dataset
mock_data = {
    "email": [
        "johndoe@gmail.com",
        "aryan.mehta@gmail.com",
        "kavya.sharma@gmail.com",
        "rohan.verma@gmail.com",
        "neha.singh@gmail.com"
    ],
    "phone": [
        "9876543210",
        "9876543211",
        "9876543212",
        "9876543213",
        "9876543214"
    ],
    "skills": [
        "python, sql, machine learning",
        "python, java, sql",
        "machine learning, python, sql, deep learning, aws",
        "java, c++",
        "python, machine learning"
    ]
}

df = pd.DataFrame(mock_data)

# 2. Run your Day 13 Feature Engineering logic over it
engineer = FeatureEngineer()
df = engineer.skill_count(df)
df = engineer.candidate_level(df)

# 3. Overwrite your CSV with the rich dataset
df.to_csv("data/processed_candidates.csv", index=False)
print("Dataset successfully fixed with 5 mock candidates!")
print(df)