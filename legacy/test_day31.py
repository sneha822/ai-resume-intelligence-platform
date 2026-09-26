import pandas as pd

from src.scoring import CandidateScorer


# Load processed candidate dataset
dataframe = pd.read_csv(
    "data/processed_candidates.csv"
)


# Create scorer
scorer = CandidateScorer()


# Calculate employability scores
dataframe = scorer.score_dataframe(
    dataframe
)


# Calculate ranking scores
dataframe = scorer.calculate_ranking_score(
    dataframe
)


print("\n=== CANDIDATE SCORING RESULTS ===")

print(
    dataframe[
        [
            "email",
            "skill_count",
            "candidate_level",
            "employability_score",
            "ranking_score"
        ]
    ]
)


# Save updated dataset
dataframe.to_csv(
    "data/processed_candidates.csv",
    index=False
)


print(
    "\nScoring completed successfully."
)