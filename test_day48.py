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
        "=== DAY 48: END-TO-END TEST ==="
    )

    # ==========================================
    # STEP 1 — Load Job Description
    # ==========================================

    jd_text = read_text_file(
        JD_PATH
    )

    print(
        "\n[1/5] Job description loaded."
    )

    # ==========================================
    # STEP 2 — Parse JD
    # ==========================================

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

    if not job_keywords:
        raise ValueError(
            "No keywords extracted from JD."
        )

    print(
        f"[2/5] JD parsed successfully."
    )

    print(
        f"Keywords found: "
        f"{len(job_keywords)}"
    )

    # ==========================================
    # STEP 3 — Discover resumes
    # ==========================================

    resume_files = [
        os.path.join(
            RESUME_DIRECTORY,
            filename
        )
        for filename
        in os.listdir(
            RESUME_DIRECTORY
        )
        if filename.endswith(
            ".txt"
        )
    ]

    if not resume_files:
        raise FileNotFoundError(
            "No resume files found."
        )

    print(
        f"[3/5] Found "
        f"{len(resume_files)} resumes."
    )

    # ==========================================
    # STEP 4 — Batch evaluation
    # ==========================================

    evaluator = (
        BatchCandidateEvaluator()
    )

    leaderboard = (
        evaluator.evaluate_batch(
            resume_files,
            job_keywords
        )
    )

    print(
        "[4/5] Batch evaluation completed."
    )

    # ==========================================
    # STEP 5 — Validate output
    # ==========================================

    required_columns = [
        "candidate",
        "match_score",
        "similarity_score",
        "status",
        "error"
    ]

    for column in required_columns:

        assert column in (
            leaderboard.columns
        ), (
            f"Missing column: {column}"
        )

    successful = leaderboard[
        leaderboard["status"]
        == "Success"
    ]

    print(
        f"[5/5] Output validation passed."
    )

    print(
        "\n=== FINAL LEADERBOARD ==="
    )

    print(
        leaderboard[
            [
                "rank",
                "candidate",
                "match_score",
                "similarity_score",
                "status"
            ]
        ].to_string(
            index=False
        )
    )

    print(
        "\nSuccessful candidates: "
        f"{len(successful)}"
    )

    print(
        "\n=== DAY 48 COMPLETE ==="
    )


if __name__ == "__main__":
    main()