import pandas as pd

from src.best_model import BestModelTrainer


df = pd.read_csv(
    "data/processed_candidates.csv"
)

comparison_df = pd.read_csv(
    "data/model_comparison.csv"
)

best_model_name = (
    comparison_df
    .sort_values(
        by="accuracy",
        ascending=False
    )
    .iloc[0]["model"]
)

print(
    f"Best Model: {best_model_name}"
)

trainer = BestModelTrainer()

model_path = trainer.train_and_save(
    df,
    best_model_name
)

print(
    f"Best model saved to: {model_path}"
)

predictor = BestModelTrainer()

prediction = predictor.predict(
    [
        5,  # skill_count
        4,  # experience_years
        5,  # project_count
        3   # certification_count
    ]
)

print(
    f"Candidate Prediction: {prediction}"
)