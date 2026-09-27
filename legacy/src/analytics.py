import pandas as pd


class CandidateAnalytics:

    def total_candidates(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return len(dataframe)

    def total_unique_emails(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return dataframe["email"].nunique()

    def missing_email_count(
        self,
        dataframe: pd.DataFrame
    ) -> int:

        return dataframe["email"].isna().sum()