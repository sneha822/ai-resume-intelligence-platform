from src.parser import ResumeParser
from src.job_description import (
    JobDescriptionParser
)
from src.job_matcher import JobMatcher
from src.match_scorer import MatchScorer


RESUME_PATH = (
    "data/raw/sample_resume.txt"
)

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
        "=== DAY 43: MATCH SCORE ==="
    )

    # ---------------------------------
    # 1. Parse resume
    # ---------------------------------

    resume_parser = ResumeParser()

    resume_data = (
        resume_parser.parse_resume(
            RESUME_PATH
        )
    )

    resume_skills = resume_data.get(
        "skills",
        []
    )

    # ---------------------------------
    # 2. Parse JD
    # ---------------------------------

    job_description = (
        read_text_file(
            JD_PATH
        )
    )

    jd_parser = (
        JobDescriptionParser()
    )

    jd_data = (
        jd_parser.parse_job_description(
            job_description
        )
    )

    jd_keywords = jd_data.get(
        "keywords",
        []
    )

    # ---------------------------------
    # 3. Match tokens
    # ---------------------------------

    matcher = JobMatcher()

    matching_result = matcher.match(
        resume_skills,
        jd_keywords
    )

    matched_tokens = (
        matching_result[
            "matched_tokens"
        ]
    )

    # ---------------------------------
    # 4. Calculate scores
    # ---------------------------------

    scorer = MatchScorer()

    score_report = (
        scorer.generate_score_report(
            resume_skills,
            jd_keywords,
            matched_tokens
        )
    )

    # ---------------------------------
    # 5. Display results
    # ---------------------------------

    print(
        "\n--- Resume Skills ---"
    )

    print(resume_skills)

    print(
        "\n--- JD Keywords ---"
    )

    print(jd_keywords)

    print(
        "\n--- Matched Tokens ---"
    )

    print(matched_tokens)

    print(
        "\n--- Match Score ---"
    )

    print(
        f"{score_report['match_score']}%"
    )

    print(
        "\n--- Similarity Score ---"
    )

    print(
        f"{score_report['similarity_score']}%"
    )

    print(
        "\n=== DAY 43 COMPLETE ==="
    )


if __name__ == "__main__":
    main()