from src.parser import ResumeParser
from src.validation import DataValidator
from src.interview_question_generator import (
    InterviewQuestionGenerator
)


RESUME_PATH = (
    "data/raw/sample_resume.txt"
)


def main() -> None:

    print("=== DAY 41 END-TO-END TEST ===")

    # --------------------------------
    # 1. Parse Resume
    # --------------------------------

    parser = ResumeParser()

    candidate = parser.parse_resume(
        RESUME_PATH
    )

    print("\n--- Candidate Data ---")

    print(
        candidate
    )

    # --------------------------------
    # 2. Validate Candidate
    # --------------------------------

    validator = DataValidator()

    is_valid = (
        validator.validate_candidate(
            candidate
        )
    )

    print("\n--- Validation ---")

    print(
        f"Valid Candidate: {is_valid}"
    )

    if not is_valid:
        raise ValueError(
            "Candidate failed validation."
        )

    # --------------------------------
    # 3. Generate Interview Questions
    # --------------------------------

    generator = (
        InterviewQuestionGenerator()
    )

    questions = (
        generator.generate_questions_with_skills(
            candidate["skills"]
        )
    )

    print(
        "\n--- Interview Questions ---"
    )

    for skill, skill_questions in (
        questions.items()
    ):

        print(
            f"\n{skill.upper()}"
        )

        for question in skill_questions:

            print(
                f"- {question}"
            )

    # --------------------------------
    # 4. Final Status
    # --------------------------------

    print(
        "\n=== END-TO-END TEST PASSED ==="
    )


if __name__ == "__main__":
    main()