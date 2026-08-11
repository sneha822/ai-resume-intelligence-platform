import pandas as pd


class CandidateScorer:
    """Calculate candidate employability and ranking scores."""

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
        Calculate score based on skill count.
        """

        return skill_count * 10

    def calculate_level_bonus(
        self,
        level: str
    ) -> int:
        """
        Calculate bonus based on candidate level.
        """

        return self.LEVEL_BONUS.get(
            level,
            0
        )

    def calculate_total_score(
        self,
        skill_count: int,
        level: str
    ) -> int:
        """
        Calculate the candidate's total score.
        """

        skill_score = self.calculate_skill_score(
            skill_count
        )

        level_bonus = self.calculate_level_bonus(
            level
        )

        return skill_score + level_bonus

    def calculate_employability_score(
        self,
        skill_count: int,
        level: str
    ) -> int:
        """
        Calculate the employability score.

        Currently this uses the existing candidate
        scoring logic as the employability score.
        """

        return self.calculate_total_score(
            skill_count,
            level
        )

    def score_dataframe(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Add employability score to every candidate.
        """

        dataframe = dataframe.copy()

        dataframe["employability_score"] = (
            dataframe.apply(
                lambda row: self.calculate_employability_score(
                    row["skill_count"],
                    row["candidate_level"]
                ),
                axis=1
            )
        )

        return dataframe

    def calculate_ranking_score(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Rank candidates using their employability score.
        """

        dataframe = dataframe.copy()

        dataframe = dataframe.sort_values(
            by="employability_score",
            ascending=False
        )

        dataframe["ranking_score"] = range(
            1,
            len(dataframe) + 1
        )

        return dataframe

    def rank_candidates(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Sort candidates from highest to lowest
        employability score.
        """

        return dataframe.sort_values(
            by="employability_score",
            ascending=False
        )