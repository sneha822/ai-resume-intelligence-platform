import pandas as pd


class DatasetSummary:

    def dataset_information(
        self,
        dataframe: pd.DataFrame
    ) -> None:

        print("\nShape")
        print(dataframe.shape)

        print("\nColumns")
        print(dataframe.columns.tolist())

        print("\nData Types")
        print(dataframe.dtypes)