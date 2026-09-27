import os
import pandas as pd
from src.best_model import BestModelTrainer


def test_day30_best_model():
    csv_path = "data/processed_candidates.csv"

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame()

    if "selection_status" not in df.columns or df["selection_status"].nunique() < 2:
        df = pd.DataFrame({
            "skill_count": [2, 5, 8, 3, 6],
            "experience_years": [1, 4, 7, 2, 5],
            "project_count": [1, 3, 6, 2, 4],
            "certification_count": [0, 2, 4, 1, 3],
            "selection_status": [1, 0, 1, 0, 1]
        })
    elif df["selection_status"].dtype == object:
        df["selection_status"] = df["selection_status"].map({"Selected": 1, "Rejected": 0}).fillna(0).astype(int)

    trainer = BestModelTrainer()
    model_path = trainer.train_and_save(df, "Logistic Regression")
    assert model_path is not None