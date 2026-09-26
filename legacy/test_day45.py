import pandas as pd

from src.parser import ResumeParser
from src.job_description import JobDescriptionParser
from src.job_matcher import JobMatcher
from src.match_scorer import MatchScorer
from src.candidate_ranker import CandidateRanker


RESUME_DIRECTORY = "data/raw"

JD_PATH = (
    "data/job_descriptions/"
    "python_data_engineer.txt"
)


def read_text_file(
    file_path: str
) -> str:
    """Read a text file."""

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def main() -> None:

    print(
        "=== DAY 45: CANDIDATE RANKING ==="
    )

    # ---------------------------------
    # 1. Parse Job Description
    # ---------------------------------

    jd_text = read_text_file(
        JD_PATH
    )

    jd_parser = (
        JobDescriptionParser()
    )

    jd_data = (
        jd_parser.parse_job_description(
            jd_text
        )
    )

    jd_keywords = jd_data.get(
        "keywords",
        []
    )

    print(
        "\nJD Keywords:"
    )

    print(jd_keywords)

    # ---------------------------------
    # 2. Initialize components
    # ---------------------------------

    resume_parser = ResumeParser()
    matcher = JobMatcher()
    scorer = MatchScorer()
    ranker = CandidateRanker()

    candidate_results = []

    # ---------------------------------
    # 3. Process candidates
    # ---------------------------------

    resume_files = [
        "sample_resume.txt",
        "candidate2.txt",
        "candidate3.txt"
    ]

    for resume_file in resume_files:

        file_path = (
            f"{RESUME_DIRECTORY}/"
            f"{resume_file}"
        )

        try:

            candidate_data = (
                resume_parser.parse_resume(
                    file_path
                )
            )

            resume_skills = (
                candidate_data.get(
                    "skills",
                    []
                )
            )

            # -------------------------
            # Match resume with JD
            # -------------------------

            matching_result = (
                matcher.match(
                    resume_skills,
                    jd_keywords
                )
            )

            matched_tokens = (
                matching_result[
                    "matched_tokens"
                ]
            )

            # -------------------------
            # Calculate score
            # -------------------------

            score_report = (
                scorer.generate_score_report(
                    resume_skills,
                    jd_keywords,
                    matched_tokens
                )
            )

            candidate_results.append(
                {
                    "email": candidate_data[
                        "email"
                    ],
                    "phone": candidate_data[
                        "phone"
                    ],
                    "match_score": (
                        score_report[
                            "match_score"
                        ]
                    ),
                    "similarity_score": (
                        score_report[
                            "similarity_score"
                        ]
                    ),
                    "matched_tokens": (
                        ", ".join(
                            matched_tokens
                        )
                    )
                }
            )

        except Exception as error:

            print(
                f"Error processing "
                f"{resume_file}: {error}"
            )

    # ---------------------------------
    # 4. Create ranking dataframe
    # ---------------------------------

    ranking_dataframe = pd.DataFrame(
        candidate_results
    )

    ranked_candidates = (
        ranker.rank_candidates(
            ranking_dataframe
        )
    )

    # ---------------------------------
    # 5. Display leaderboard
    # ---------------------------------

    print(
        "\n--- CANDIDATE RANKING ---"
    )

    print(
        ranked_candidates[
            [
                "job_rank",
                "email",
                "match_score",
                "similarity_score",
                "matched_tokens"
            ]
        ].to_string(
            index=False
        )
    )

    print(
        "\n=== DAY 45 COMPLETE ==="
    )


if __name__ == "__main__":
    main()