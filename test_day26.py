import pandas as pd

from src.model_trainer import (
    RoleClassifierTrainer
)

df = pd.read_csv(
    "data/processed_candidates.csv"
)

trainer = RoleClassifierTrainer()

accuracy = trainer.train(df)

print(
    f"Model Accuracy: {accuracy:.2f}"
)