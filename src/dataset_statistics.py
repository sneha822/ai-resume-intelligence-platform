import pandas as pd


class DatasetStatistics:

    def numerical_summary(
        self,
        dataframe: pd.DataFrame
    ):

        return dataframe[
            [
                "skill_count",
                "experience_years",
                "project_count",
                "certification_count"
            ]
        ].describe()