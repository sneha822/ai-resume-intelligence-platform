import pandas as pd


class CandidateDatasetBuilder:

    def add_numerical_features(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        if "experience_years" not in dataframe.columns:
            dataframe["experience_years"] = 0

        if "project_count" not in dataframe.columns:
            dataframe["project_count"] = 0

        if "certification_count" not in dataframe.columns:
            dataframe["certification_count"] = 0

        return dataframe