import json

from src.ai.llm_client import LLMClient
from src.ai.prompts import (
    RESUME_EXTRACTION_SYSTEM_PROMPT
)
from src.ai.schemas import CandidateProfile


class AIResumeExtractor:
    """Extract structured candidate information using an LLM."""

    def __init__(
        self,
        llm_client=None
    ):

        self.llm_client = (
            llm_client
            or LLMClient()
        )

    def build_prompt(
        self,
        resume_text: str
    ) -> str:
        """Build structured extraction prompt."""

        if not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty."
            )

        return f"""
Extract structured candidate information
from the resume below.

Return ONLY valid JSON.

Required JSON structure:

{{
    "name": null,
    "email": null,
    "phone": null,

    "skills": [],

    "experience": [
        {{
            "company": null,
            "role": null,
            "duration": null,
            "responsibilities": [],
            "achievements": []
        }}
    ],

    "education": [
        {{
            "degree": null,
            "field": null,
            "institution": null,
            "graduation_year": null
        }}
    ],

    "certifications": [],

    "projects": []
}}

Extraction rules:

1. Extract only information explicitly supported
   by the resume.
2. Never invent missing information.
3. Use null when a single value is unavailable.
4. Use [] when a list has no available information.
5. Preserve measurable achievements.
6. Preserve technologies and tools as skills.
7. Keep different jobs as separate experience entries.
8. Keep different education records separate.
9. Preserve project names when available.
10. Return valid JSON only.

Resume:

--- BEGIN RESUME ---

{resume_text}

--- END RESUME ---
"""

    def parse_response(
        self,
        response: str
    ) -> CandidateProfile:
        """Convert LLM JSON response into a candidate profile."""

        if not response.strip():
            raise ValueError(
                "LLM returned an empty response."
            )

        try:

            data = json.loads(
                response
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                "LLM response was not valid JSON."
            ) from error

        if not isinstance(
            data,
            dict
        ):

            raise ValueError(
                "LLM response must be a JSON object."
            )

        return CandidateProfile.from_dict(
            data
        )

    def extract(
        self,
        resume_text: str
    ) -> CandidateProfile:
        """Extract a structured candidate profile."""

        prompt = self.build_prompt(
            resume_text
        )

        response = self.llm_client.generate(
            prompt=prompt,
            system_prompt=(
                RESUME_EXTRACTION_SYSTEM_PROMPT
            )
        )

        return self.parse_response(
            response
        )