import pandas as pd

class CandidateEDA:
    """
    Exploratory Data Analysis (EDA) module for the AI Resume Intelligence Platform.
    Handles descriptive statistics, data quality checks, and feature distributions.
    """

    def level_distribution(self, dataframe: pd.DataFrame) -> pd.Series:
        """Calculates the frequency distribution of candidate experience levels."""
        if "candidate_level" not in dataframe.columns:
            return pd.Series(dtype=int)
        return dataframe["candidate_level"].value_counts()

    def total_candidates(self, dataframe: pd.DataFrame) -> int:
        """Returns the total number of candidate records in the dataset."""
        return len(dataframe)

    def unique_emails(self, dataframe: pd.DataFrame) -> int:
        """Returns the number of unique candidates based on email addresses."""
        if "email" not in dataframe.columns:
            return 0
        return dataframe["email"].nunique()

    def missing_values(self, dataframe: pd.DataFrame) -> pd.Series:
        """Counts missing (null) entries across all columns in the dataframe."""
        return dataframe.isnull().sum()

    def top_skill(self, skill_counts: dict) -> str:
        """Identifies the single most frequently occurring skill from a frequency dictionary."""
        if not skill_counts:
            return "No skills found"
        return max(skill_counts, key=skill_counts.get)