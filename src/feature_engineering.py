import pandas as pd

class FeatureEngineer:
    def skill_count(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Counts the number of skills for each candidate and adds it as a new column."""
        dataframe["skill_count"] = (
            dataframe["skills"]
            .astype(str)
            .apply(lambda skills: len([skill for skill in skills.split(",") if skill.strip()]))
        )
        return dataframe

    def candidate_level(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Classifies candidates into tiers based on their skill count."""
        def classify(count: int):
            if count <= 2:
                return "Beginner"
            elif count <= 4:
                return "Intermediate"
            return "Advanced"

        dataframe["candidate_level"] = dataframe["skill_count"].apply(classify)
        return dataframe