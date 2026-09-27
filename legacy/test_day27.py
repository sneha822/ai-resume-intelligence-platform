import pandas as pd

from src.random_forest_trainer import RandomForestTrainer


df = pd.read_csv(
    "data/processed_candidates.csv"
)

trainer = RandomForestTrainer()

accuracy = trainer.train(
    df
)

print(
    f"Random Forest Accuracy: {accuracy:.2f}"
)