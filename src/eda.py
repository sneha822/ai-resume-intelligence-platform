import pandas as pd

class CandidateEDA:

    def total_candidates(self, dataframe: pd.DataFrame) -> int:
        """Returns the total number of candidate records."""
        return len(dataframe)

    def unique_emails(self, dataframe: pd.DataFrame) -> int:
        """Returns the number of unique candidates based on email."""
        return dataframe["email"].nunique()

    def missing_values(self, dataframe: pd.DataFrame) -> pd.Series:
        """Counts missing entries per column."""
        return dataframe.isnull().sum()

    def top_skill(self, skill_counts: dict) -> str:
        """Identifies the single most frequently occurring skill."""
        if not skill_counts:
            return "No skills found"
        return max(skill_counts, key=skill_counts.get)