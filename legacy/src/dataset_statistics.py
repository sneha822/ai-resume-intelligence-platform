import pandas as pd


class DatasetStatistics:

    def numerical_summary(
        self,
        dataframe: pd.DataFrame
    ):
        expected_columns = [
            "skill_count",
            "experience_years",
            "project_count",
            "certification_count"
        ]
        
        # Filter to only keep columns present in the input dataframe
        available_columns = [
            col for col in expected_columns if col in dataframe.columns
        ]

        if not available_columns:
            # Fallback to all numeric columns in the DataFrame if none match
            return dataframe.select_dtypes(include=["number"]).describe()

        return dataframe[available_columns].describe()