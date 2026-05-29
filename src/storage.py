import pandas as pd


class DataStorage:

    def save_candidates(
        self,
        candidate_data,
        file_path
    ):

        df = pd.DataFrame(candidate_data)

        df.to_csv(
            file_path,
            index=False
        )

        print("Data saved successfully.")