import pandas as pd

from src.model_comparison import ModelComparator


df = pd.read_csv(
    "data/processed_candidates.csv"
)

comparator = ModelComparator()

results = comparator.compare_models(
    df
)

results_df = pd.DataFrame(
    list(results.items()),
    columns=["model", "accuracy"]
)

results_df.to_csv(
    "data/model_comparison.csv",
    index=False
)

print("\n=== MODEL COMPARISON ===")
print(results_df)

best_model = max(
    results,
    key=results.get
)

print("\n=== BEST MODEL ===")
print(
    f"{best_model} -> {results[best_model]:.2f}"
)