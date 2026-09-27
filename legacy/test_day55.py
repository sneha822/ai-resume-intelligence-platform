import pytest
from src.ai.candidate_evaluator import CandidateEvaluator


class InvalidEvidenceLLMClient:
    def generate(self, prompt, system_prompt=None):
        return """
        {
            "overall_score": 80,
            "fit_level": "Good Fit",
            "strengths": ["Python"],
            "skill_gaps": [],
            "strength_evidence": [
                {
                    "claim": "",
                    "evidence": "Has 3 years of Python experience.",
                    "category": "technical"
                }
            ],
            "gap_evidence": [],
            "experience_fit": "Good",
            "technical_fit": "Good",
            "reasoning": "Solid candidate."
        }
        """


def test_invalid_evidence_validation():
    evaluator = CandidateEvaluator(llm_client=InvalidEvidenceLLMClient())
    
    with pytest.raises(ValueError) as exc_info:
        evaluator.evaluate({"name": "Test Candidate"}, "Job Description")

    assert "Strength evidence contains empty claim." in str(exc_info.value)