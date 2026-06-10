import pandas as pd


class FeatureEngineer:

    def skill_count(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        dataframe["skill_count"] = (
            dataframe["skills"]
            .astype(str)
            .apply(
                lambda skills:
                len(
                    [
                        skill
                        for skill in skills.split(",")
                        if skill.strip()
                    ]
                )
            )
        )

        return dataframe