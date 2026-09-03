import json

from src.ai.llm_client import LLMClient
from src.ai.prompts import (
    CANDIDATE_EVALUATION_SYSTEM_PROMPT,
    build_candidate_evaluation_prompt
)
from src.ai.schemas import CandidateEvaluation


class CandidateEvaluator:
    """
    Evaluates how well a candidate fits a specific job description
    using LLM-based semantic reasoning.
    """

    def __init__(self, llm_client=None):
        self.llm_client = llm_client or LLMClient()

    def build_prompt(self, candidate, job_description):
        return build_candidate_evaluation_prompt(
            candidate,
            job_description
        )

    def parse_response(self, response):
        try:
            data = json.loads(response)
        except json.JSONDecodeError as error:
            raise ValueError(
                "LLM returned invalid JSON."
            ) from error

        if not isinstance(data, dict):
            raise ValueError(
                "LLM response must be a JSON object."
            )

        return CandidateEvaluation.from_dict(data)

    def evaluate(self, candidate, job_description):

        if not candidate:
            raise ValueError("Candidate profile cannot be empty.")

        if not job_description:
            raise ValueError(
                "Job description cannot be empty."
            )

        prompt = self.build_prompt(
            candidate,
            job_description
        )

        response = self.llm_client.generate(
            prompt,
            system_prompt=CANDIDATE_EVALUATION_SYSTEM_PROMPT
        )

        return self.parse_response(response)