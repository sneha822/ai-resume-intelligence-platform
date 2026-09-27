import pandas as pd
from sklearn.model_selection import train_test_split


class CandidateDataSplitter:

    def split_dataset(
        self,
        dataframe: pd.DataFrame,
        test_size: float = 0.2,
        random_state: int = 42
    ):

        train_df, test_df = train_test_split(
            dataframe,
            test_size=test_size,
            random_state=random_state
        )

        return train_df, test_df