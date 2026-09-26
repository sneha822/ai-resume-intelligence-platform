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

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def main() -> None:

    print(
        "=== DAY 47: ERROR HANDLING TEST ==="
    )

    # ------------------------------------------
    # 1. Parse JD
    # ------------------------------------------

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
        "\nJD Keywords:"
    )

    print(
        job_keywords
    )

    # ------------------------------------------
    # 2. Find resumes
    # ------------------------------------------

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

    print(
        f"\nResumes found: "
        f"{len(resume_files)}"
    )

    # ------------------------------------------
    # 3. Run protected batch
    # ------------------------------------------

    evaluator = (
        BatchCandidateEvaluator()
    )

    try:

        leaderboard = (
            evaluator.evaluate_batch(
                resume_files,
                job_keywords
            )
        )

        print(
            "\n=== BATCH RESULTS ==="
        )

        if leaderboard.empty:

            print(
                "No candidates were evaluated."
            )

        else:

            print(
                leaderboard[
                    [
                        "rank",
                        "candidate",
                        "match_score",
                        "status",
                        "error"
                    ]
                ].to_string(
                    index=False
                )
            )

    except Exception as error:

        print(
            f"\nBatch evaluation failed: "
            f"{error}"
        )

    print(
        "\n=== DAY 47 COMPLETE ==="
    )


if __name__ == "__main__":
    main()