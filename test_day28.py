import pandas as pd
from src.selection_predictor import CandidateSelectionPredictor

# 1. Load data
df = pd.read_csv("data/processed_candidates.csv")

# 2. Train model
predictor = CandidateSelectionPredictor()
accuracy = predictor.train(df)
print(f"Selection Model Accuracy: {accuracy:.2f}")

# 3. Predict sample candidate (removes UserWarning)
sample_candidate = {
    "skill_count": 4,
    "experience_years": 3,
    "project_count": 2,
    "certification_count": 1
}

result = predictor.predict_candidate(sample_candidate)
print(f"Candidate Selection: {result}")