import os
import pandas as pd

from src.parser import ResumeParser
from src.job_matcher import JobMatcher
from src.match_scorer import MatchScorer
from src.logger import logger


class BatchCandidateEvaluator:
    """Evaluate multiple resumes against one job description."""

    def __init__(self) -> None:
        self.resume_parser = ResumeParser()
        self.matcher = JobMatcher()
        self.scorer = MatchScorer()

    def evaluate_candidate(
        self,
        file_path: str,
        job_keywords: list
    ) -> dict:
        """
        Evaluate one candidate against a job description.
        """

        # ------------------------------------------
        # File validation
        # ------------------------------------------

        if not file_path:
            raise ValueError(
                "Resume file path is empty."
            )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Resume file not found: {file_path}"
            )

        if not job_keywords:
            raise ValueError(
                "Job description contains no keywords."
            )

        logger.info(
            f"Starting candidate evaluation: {file_path}"
        )

        # ------------------------------------------
        # Resume parsing
        # ------------------------------------------

        candidate_data = (
            self.resume_parser.parse_resume(
                file_path
            )
        )

        if not candidate_data:
            raise ValueError(
                "Resume parser returned empty data."
            )

        email = candidate_data.get(
            "email"
        )

        skills = candidate_data.get(
            "skills",
            []
        )

        # ------------------------------------------
        # Candidate validation
        # ------------------------------------------

        if not email:
            logger.warning(
                f"No email detected in resume: {file_path}"
            )

        if not skills:
            logger.warning(
                f"No skills detected in resume: {file_path}"
            )

        # ------------------------------------------
        # Matching
        # ------------------------------------------

        matching_result = self.matcher.match(
            skills,
            job_keywords
        )

        if not matching_result:
            raise ValueError(
                "Matching engine returned no result."
            )

        matched_tokens = matching_result.get(
            "matched_tokens",
            []
        )

        missing_tokens = matching_result.get(
            "missing_tokens",
            []
        )

        # ------------------------------------------
        # Scoring
        # ------------------------------------------

        score_report = (
            self.scorer.generate_score_report(
                skills,
                job_keywords,
                matched_tokens
            )
        )

        if not score_report:
            raise ValueError(
                "Scoring engine returned no result."
            )

        match_score = score_report.get(
            "match_score",
            0
        )

        similarity_score = score_report.get(
            "similarity_score",
            0
        )

        logger.info(
            f"Candidate evaluation completed: {file_path}"
        )

        return {
            "candidate": os.path.basename(
                file_path
            ),
            "email": email or "Not detected",
            "match_score": match_score,
            "similarity_score": similarity_score,
            "matched_skills": ", ".join(
                matched_tokens
            ),
            "missing_skills": ", ".join(
                missing_tokens
            ),
            "status": "Success",
            "error": ""
        }

    def evaluate_batch(
        self,
        file_paths: list,
        job_keywords: list
    ) -> pd.DataFrame:
        """
        Evaluate an entire batch of candidates.

        One failed candidate does not stop
        the remaining candidates.
        """

        if not file_paths:
            logger.warning(
                "Batch evaluation requested with no resumes."
            )

            return pd.DataFrame()

        if not job_keywords:
            logger.error(
                "Batch evaluation stopped: "
                "no JD keywords available."
            )

            raise ValueError(
                "Cannot evaluate candidates "
                "without JD keywords."
            )

        results = []

        logger.info(
            f"Starting batch evaluation for "
            f"{len(file_paths)} candidates."
        )

        for file_path in file_paths:

            try:

                result = self.evaluate_candidate(
                    file_path,
                    job_keywords
                )

                results.append(
                    result
                )

            except Exception as error:

                logger.error(
                    f"Failed to evaluate "
                    f"{file_path}: {error}"
                )

                results.append(
                    {
                        "candidate": os.path.basename(
                            file_path
                        ),
                        "email": "Not available",
                        "match_score": 0.0,
                        "similarity_score": 0.0,
                        "matched_skills": "",
                        "missing_skills": "",
                        "status": "Failed",
                        "error": str(error)
                    }
                )

        dataframe = pd.DataFrame(
            results
        )

        if dataframe.empty:
            logger.warning(
                "Batch evaluation produced no results."
            )

            return dataframe

        # ------------------------------------------
        # Rank successful results
        # ------------------------------------------

        dataframe = dataframe.sort_values(
            by="match_score",
            ascending=False
        ).reset_index(
            drop=True
        )

        dataframe["rank"] = (
            dataframe.index + 1
        )

        successful = (
            dataframe["status"]
            == "Success"
        ).sum()

        failed = (
            dataframe["status"]
            == "Failed"
        ).sum()

        logger.info(
            f"Batch evaluation completed. "
            f"Successful: {successful}, "
            f"Failed: {failed}"
        )

        return dataframe