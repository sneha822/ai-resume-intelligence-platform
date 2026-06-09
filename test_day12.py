import pandas as pd

from src.eda import CandidateEDA

from src.skill_analysis import (
    SkillAnalyzer
)

df = pd.read_csv(
    "data/processed_candidates.csv"
)

eda = CandidateEDA()

analyzer = SkillAnalyzer()

skill_counts = (
    analyzer.skill_frequency(df)
)

print(
    "Total Candidates:",
    eda.total_candidates(df)
)

print(
    "Unique Emails:",
    eda.unique_emails(df)
)

print(
    "Missing Values:"
)

print(
    eda.missing_values(df)
)

print(
    "Top Skill:",
    eda.top_skill(skill_counts)
)