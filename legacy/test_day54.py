import pytest
from src.ai.schemas import CandidateEvaluation
from src.ai.candidate_evaluator import CandidateEvaluator


class FakeLLMClient:

    def generate(self, prompt, system_prompt=None):
        return """
        {
            "overall_score": 87,
            "fit_level": "Strong Fit",
            "strengths": [
                "Strong Python experience",
                "Relevant backend development experience",
                "Experience with AWS"
            ],
            "skill_gaps": [
                "Limited evidence of Kubernetes experience"
            ],
            "experience_fit": "Strong",
            "technical_fit": "Strong",
            "reasoning": "The candidate demonstrates strong backend development skills with Python, AWS, and relevant project experience."
        }
        """


def test_candidate_evaluation():
    candidate = {
        "name": "John Doe",
        "skills": ["Python", "FastAPI", "AWS", "SQL"],
        "experience": [
            {
                "company": "ABC Technologies",
                "role": "Backend Developer",
                "duration": "3 years"
            }
        ],
        "projects": [
            {
                "name": "Customer Analytics Platform",
                "technologies": ["Python", "FastAPI", "PostgreSQL"]
            }
        ]
    }

    job_description = """
    Looking for a backend developer with Python,
    FastAPI, AWS and cloud experience.
    """

    evaluator = CandidateEvaluator(llm_client=FakeLLMClient())
    result = evaluator.evaluate(candidate, job_description)

    assert result.overall_score == 87
    assert result.fit_level == "Strong Fit"
    assert "Strong Python experience" in result.strengths
    assert len(result.skill_gaps) == 1
    assert result.technical_fit == "Strong"


def test_invalid_score():
    with pytest.raises(ValueError):
        CandidateEvaluation.from_dict({
            "overall_score": 150,
            "fit_level": "Strong Fit"
        })