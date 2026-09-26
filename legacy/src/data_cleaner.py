import pandas as pd


class CandidateDataCleaner:

    def load_data(
        self,
        file_path: str
    ) -> pd.DataFrame:

        return pd.read_csv(file_path)

    def remove_duplicates(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        return dataframe.drop_duplicates()

    def remove_missing_emails(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        return dataframe.dropna(
            subset=["email"]
        )

    def standardize_emails(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        dataframe.loc[:, "email"] = (
            dataframe["email"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        return dataframe

    def standardize_skills(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        dataframe.loc[:, "skills"] = (
            dataframe["skills"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        return dataframe

    def clean_dataset(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        dataframe = self.remove_duplicates(
            dataframe
        )

        dataframe = self.remove_missing_emails(
            dataframe
        )

        dataframe = self.standardize_emails(
            dataframe
        )

        dataframe = self.standardize_skills(
            dataframe
        )

        return dataframe