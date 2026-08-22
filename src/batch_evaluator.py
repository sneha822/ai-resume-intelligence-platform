import os
import pandas as pd

from src.parser import ResumeParser
from src.job_matcher import JobMatcher
from src.match_scorer import MatchScorer


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
        """Evaluate one candidate against the selected JD."""

        candidate_data = (
            self.resume_parser.parse_resume(
                file_path
            )
        )

        resume_skills = candidate_data.get(
            "skills",
            []
        )

        matching_result = self.matcher.match(
            resume_skills,
            job_keywords
        )

        matched_tokens = matching_result[
            "matched_tokens"
        ]

        score_report = (
            self.scorer.generate_score_report(
                resume_skills,
                job_keywords,
                matched_tokens
            )
        )

        return {
            "candidate": os.path.basename(
                file_path
            ),
            "email": candidate_data.get(
                "email",
                ""
            ),
            "match_score": score_report[
                "match_score"
            ],
            "similarity_score": score_report[
                "similarity_score"
            ],
            "matched_skills": ", ".join(
                matched_tokens
            ),
            "missing_skills": ", ".join(
                matching_result[
                    "missing_tokens"
                ]
            )
        }

    def evaluate_batch(
        self,
        file_paths: list,
        job_keywords: list
    ) -> pd.DataFrame:
        """Evaluate an entire batch of candidates."""

        results = []

        for file_path in file_paths:

            try:
                result = self.evaluate_candidate(
                    file_path,
                    job_keywords
                )

                results.append(result)

            except Exception as error:

                results.append(
                    {
                        "candidate": os.path.basename(
                            file_path
                        ),
                        "email": "",
                        "match_score": 0.0,
                        "similarity_score": 0.0,
                        "matched_skills": "",
                        "missing_skills": "",
                        "error": str(error)
                    }
                )

        dataframe = pd.DataFrame(
            results
        )

        if dataframe.empty:
            return dataframe

        dataframe = dataframe.sort_values(
            by="match_score",
            ascending=False
        ).reset_index(
            drop=True
        )

        dataframe["rank"] = (
            dataframe.index + 1
        )

        return dataframe