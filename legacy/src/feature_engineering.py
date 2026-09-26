import pandas as pd

class FeatureEngineer:
    def skill_count(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Counts the number of skills for each candidate safely using .loc"""
        dataframe.loc[:, "skill_count"] = (
            dataframe["skills"]
            .astype(str)
            .apply(lambda skills: len([skill for skill in skills.split(",") if skill.strip()]))
        )
        return dataframe

    def candidate_level(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Classifies candidates into tiers based on their skill count safely using .loc"""
        def classify(count: int) -> str:
            if count <= 2:
                return "Beginner"
            elif count <= 4:
                return "Intermediate"
            return "Advanced"

        dataframe.loc[:, "candidate_level"] = dataframe["skill_count"].apply(classify)
        return dataframe