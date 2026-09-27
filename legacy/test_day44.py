from src.parser import ResumeParser
from src.job_description import (
    JobDescriptionParser
)
from src.job_matcher import JobMatcher
from src.match_scorer import MatchScorer
from src.match_explainer import MatchExplainer


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
        "=== DAY 44: MATCH EXPLANATION ==="
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

    # ---------------------------------
    # 4. Calculate score
    # ---------------------------------

    scorer = MatchScorer()

    score_report = (
        scorer.generate_score_report(
            resume_skills,
            jd_keywords,
            matching_result[
                "matched_tokens"
            ]
        )
    )

    # ---------------------------------
    # 5. Generate explanation
    # ---------------------------------

    explainer = MatchExplainer()

    explanation = (
        explainer.explain_match(
            matched_tokens=(
                matching_result[
                    "matched_tokens"
                ]
            ),
            missing_tokens=(
                matching_result[
                    "missing_tokens"
                ]
            ),
            extra_tokens=(
                matching_result[
                    "extra_tokens"
                ]
            ),
            match_score=(
                score_report[
                    "match_score"
                ]
            )
        )
    )

    # ---------------------------------
    # 6. Display results
    # ---------------------------------

    print(
        "\n--- MATCH SCORE ---"
    )

    print(
        f"{explanation['match_score']}%"
    )

    print(
        "\n--- MATCHED SKILLS ---"
    )

    for skill in explanation[
        "matched_tokens"
    ]:

        print(
            f"✓ {skill}"
        )

    print(
        "\n--- MISSING REQUIREMENTS ---"
    )

    for skill in explanation[
        "missing_tokens"
    ]:

        print(
            f"✗ {skill}"
        )

    print(
        "\n--- ADDITIONAL RESUME SKILLS ---"
    )

    for skill in explanation[
        "extra_tokens"
    ]:

        print(
            f"+ {skill}"
        )

    print(
        "\n--- MATCH BREAKDOWN ---"
    )

    print(
        f"Required skills: "
        f"{explanation['total_required_skills']}"
    )

    print(
        f"Matched: "
        f"{explanation['matched_count']}"
    )

    print(
        f"Missing: "
        f"{explanation['missing_count']}"
    )

    print(
        f"Additional: "
        f"{explanation['extra_count']}"
    )

    print(
        "\n--- EXPLANATION ---"
    )

    print(
        explainer.generate_summary(
            explanation
        )
    )

    print(
        "\n=== DAY 44 COMPLETE ==="
    )


if __name__ == "__main__":
    main()