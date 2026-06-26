import pandas as pd
from src.scoring import CandidateScorer

# 1. Load the engineered dataset
df = pd.read_csv("data/processed_candidates.csv")

# 2. Initialize the scorer
scorer = CandidateScorer()

# 3. Score the candidates
df = scorer.score_dataframe(df)

# 4. Rank the candidates
ranked_df = scorer.rank_candidates(df)

print("\n=== Candidate Ranking ===")
print(ranked_df[["email", "candidate_score"]])

# 5. Save the updated dataset with scores
ranked_df.to_csv("data/processed_candidates.csv", index=False)
print("\nSuccessfully saved scores to data/processed_candidates.csv")