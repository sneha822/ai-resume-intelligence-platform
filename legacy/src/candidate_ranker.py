import pandas as pd


class CandidateRanker:
    """Ranks candidates for a specific job description."""

    def rank_candidates(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Rank candidates by job-specific match score.
        """

        if dataframe.empty:
            return dataframe.copy()

        ranked_dataframe = (
            dataframe
            .sort_values(
                by="match_score",
                ascending=False
            )
            .reset_index(
                drop=True
            )
        )

        ranked_dataframe[
            "job_rank"
        ] = (
            ranked_dataframe
            .index
            + 1
        )

        return ranked_dataframe