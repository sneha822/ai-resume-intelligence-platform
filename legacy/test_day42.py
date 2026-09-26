from src.parser import ResumeParser
from src.job_description import (
    JobDescriptionParser
)
from src.job_matcher import JobMatcher


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
        "=== DAY 42: RESUME ↔ JD MATCHING ==="
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
    # 2. Parse job description
    # ---------------------------------

    job_description = read_text_file(
        JD_PATH
    )

    jd_parser = JobDescriptionParser()

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
    # 3. Match resume against JD
    # ---------------------------------

    matcher = JobMatcher()

    result = matcher.match(
        resume_skills,
        jd_keywords
    )

    # ---------------------------------
    # 4. Display results
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
        "\n--- Matching Tokens ---"
    )

    for token in result[
        "matched_tokens"
    ]:

        print(
            f"✓ {token}"
        )

    print(
        "\n--- Missing JD Requirements ---"
    )

    for token in result[
        "missing_tokens"
    ]:

        print(
            f"✗ {token}"
        )

    print(
        "\n--- Additional Resume Skills ---"
    )

    for token in result[
        "extra_tokens"
    ]:

        print(
            f"+ {token}"
        )

    print(
        "\n=== DAY 42 COMPLETE ==="
    )


if __name__ == "__main__":
    main()