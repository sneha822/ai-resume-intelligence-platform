from src.parser import ResumeParser
from src.interview_report import (
    InterviewReportGenerator
)


RESUME_PATH = (
    "data/raw/sample_resume.txt"
)


def main() -> None:

    print(
        "=== DAY 42 INTERVIEW REPORT ==="
    )

    # -----------------------------
    # 1. Parse candidate resume
    # -----------------------------

    parser = ResumeParser()

    candidate = parser.parse_resume(
        RESUME_PATH
    )

    print(
        "\nCandidate Skills:"
    )

    print(
        candidate["skills"]
    )

    # -----------------------------
    # 2. Generate interview report
    # -----------------------------

    report_generator = (
        InterviewReportGenerator()
    )

    report = (
        report_generator.generate_report(
            candidate
        )
    )

    # -----------------------------
    # 3. Display report
    # -----------------------------

    print(
        "\n=== INTERVIEW REPORT ==="
    )

    print(
        f"Email: {report['email']}"
    )

    print(
        f"Phone: {report['phone']}"
    )

    print(
        f"Skills: {report['skills']}"
    )

    print(
        "\n--- Technical Questions ---"
    )

    for skill, questions in (
        report["interview_questions"].items()
    ):

        print(
            f"\n{skill.upper()}"
        )

        for number, question in enumerate(
            questions,
            start=1
        ):

            print(
                f"{number}. {question}"
            )


if __name__ == "__main__":
    main()