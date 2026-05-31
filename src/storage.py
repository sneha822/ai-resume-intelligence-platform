import pandas as pd


class DataStorage:

    def save_candidates(
        self,
        candidate_data: list,
        file_path: str
    ) -> None:

        dataframe = pd.DataFrame(candidate_data)

        dataframe.to_csv(
            file_path,
            index=False
        )

        print(
            f"Data saved successfully to {file_path}"
        )