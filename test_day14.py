import pandas as pd

from src.scoring import CandidateScorer

df = pd.read_csv(
    "data/processed_candidates.csv"
)

scorer = CandidateScorer()

df = scorer.score_dataframe(df)

print(df)

df.to_csv(
    "data/processed_candidates.csv",
    index=False
)