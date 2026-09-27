from typing import Dict, List

from src.interview_question_generator import (
    InterviewQuestionGenerator
)


class InterviewReportGenerator:
    """Generate an interview preparation report for a candidate."""

    def __init__(self) -> None:

        self.question_generator = (
            InterviewQuestionGenerator()
        )

    def generate_questions(
        self,
        skills: List[str]
    ) -> Dict[str, List[str]]:
        """Generate interview questions grouped by skill."""

        return (
            self.question_generator
            .generate_questions_with_skills(
                skills
            )
        )

    def generate_report(
        self,
        candidate_data: dict
    ) -> dict:
        """Create a structured interview report."""

        skills = candidate_data.get(
            "skills",
            []
        )

        questions = self.generate_questions(
            skills
        )

        return {
            "email": candidate_data.get(
                "email"
            ),
            "phone": candidate_data.get(
                "phone"
            ),
            "skills": skills,
            "interview_questions": questions
        }