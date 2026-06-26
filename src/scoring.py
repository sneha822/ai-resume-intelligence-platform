import pandas as pd


class CandidateScorer:

    LEVEL_BONUS = {
        "Beginner": 10,
        "Intermediate": 30,
        "Advanced": 50
    }

    def calculate_skill_score(
        self,
        skill_count: int
    ) -> int:
        """
        Calculate score from skill count.
        """

        return skill_count * 10

    def calculate_level_bonus(
        self,
        level: str
    ) -> int:
        """
        Add level-based bonus.
        """

        return self.LEVEL_BONUS.get(
            level,
            0
        )
    def rank_candidates(
    self,
    dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Sort candidates by score.
        """

        return dataframe.sort_values(
           by="candidate_score",
           ascending=False
    )

    def calculate_total_score(
        self,
        skill_count: int,
        level: str
    ) -> int:
        """
        Generate final candidate score.
        """

        return (
            self.calculate_skill_score(
                skill_count
            )
            +
            self.calculate_level_bonus(
                level
            )
        )

    def score_dataframe(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        dataframe.loc[:, "candidate_score"] = (
            dataframe.apply(
                lambda row:
                self.calculate_total_score(
                    row["skill_count"],
                    row["candidate_level"]
                ),
                axis=1
            )
        )

        return dataframe