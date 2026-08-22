import os

from src.job_description import (
    JobDescriptionParser
)

from src.batch_evaluator import (
    BatchCandidateEvaluator
)


JD_PATH = (
    "data/job_descriptions/"
    "python_data_engineer.txt"
)

RESUME_DIRECTORY = "data/raw"


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
        "=== DAY 46: BATCH CANDIDATE EVALUATION ==="
    )

    # ---------------------------------
    # 1. Parse selected JD
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

    job_keywords = jd_data.get(
        "keywords",
        []
    )

    print(
        "\nJob Description Keywords:"
    )

    print(job_keywords)

    # ---------------------------------
    # 2. Find candidate resumes
    # ---------------------------------

    resume_files = []

    for filename in os.listdir(
        RESUME_DIRECTORY
    ):

        if filename.endswith(
            ".txt"
        ):

            resume_files.append(
                os.path.join(
                    RESUME_DIRECTORY,
                    filename
                )
            )

    # ---------------------------------
    # 3. Evaluate batch
    # ---------------------------------

    evaluator = (
        BatchCandidateEvaluator()
    )

    leaderboard = (
        evaluator.evaluate_batch(
            resume_files,
            job_keywords
        )
    )

    # ---------------------------------
    # 4. Display leaderboard
    # ---------------------------------

    print(
        "\n=== CANDIDATE LEADERBOARD ==="
    )

    print(
        leaderboard[
            [
                "rank",
                "candidate",
                "email",
                "match_score",
                "similarity_score",
                "matched_skills",
                "missing_skills"
            ]
        ].to_string(
            index=False
        )
    )

    print(
        "\n=== DAY 46 COMPLETE ==="
    )


if __name__ == "__main__":
    main()