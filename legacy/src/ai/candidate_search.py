import json
import re

from src.ai.llm_client import LLMClient
from src.ai.schemas import CandidateSearchQuery
from src.ai.prompts import (
    NATURAL_LANGUAGE_SEARCH_SYSTEM_PROMPT,
    build_natural_language_search_prompt,
)


class NaturalLanguageCandidateSearch:
    """
    Converts natural-language recruiter queries into structured
    search filters and searches the candidate knowledge base.
    """

    def __init__(self, knowledge_base, llm_client=None):
        self.knowledge_base = knowledge_base
        self.llm_client = llm_client or LLMClient()

    def parse_query(self, question: str) -> CandidateSearchQuery:
        """Convert natural language into a structured search query."""

        prompt = build_natural_language_search_prompt(question)

        response = self.llm_client.generate(
            prompt,
            system_prompt=NATURAL_LANGUAGE_SEARCH_SYSTEM_PROMPT,
        )

        try:
            data = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM returned invalid JSON for the search query."
            ) from exc

        return CandidateSearchQuery.from_dict(data)

    def _extract_experience_years(self, profile) -> float:
        """
        Estimate total experience from experience entries.

        Supports common duration formats such as:
        '3 years'
        '3+ years'
        '2 years'
        """

        total_years = 0.0
        
        # Extract experience list whether profile is an object or dict
        if hasattr(profile, "experience"):
            experiences = getattr(profile, "experience", []) or []
        elif isinstance(profile, dict):
            experiences = profile.get("experience", []) or []
        else:
            experiences = []

        for experience in experiences:
            if hasattr(experience, "duration"):
                duration = getattr(experience, "duration", "") or ""
            elif isinstance(experience, dict):
                duration = experience.get("duration", "") or ""
            else:
                duration = ""

            if not duration:
                continue

            match = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*years?", str(duration).lower())

            if match:
                total_years += float(match.group(1))

        return total_years

    def _candidate_matches(self, candidate, query: CandidateSearchQuery):
        # Extract candidate_id and profile safely whether candidate is a dict or CandidateRecord object
        if hasattr(candidate, "profile"):
            profile = candidate.profile
            candidate_id = getattr(candidate, "candidate_id", None)
        elif isinstance(candidate, dict):
            profile = candidate.get("profile")
            candidate_id = candidate.get("candidate_id")
        else:
            profile = candidate
            candidate_id = getattr(candidate, "candidate_id", None)

        # Extract skills safely
        if hasattr(profile, "skills"):
            raw_skills = getattr(profile, "skills", []) or []
        elif isinstance(profile, dict):
            raw_skills = profile.get("skills", []) or []
        else:
            raw_skills = []

        candidate_skills = {
            str(skill).lower()
            for skill in raw_skills
        }

        # Skill filtering
        if query.skills:
            for required_skill in query.skills:
                if not any(
                    required_skill in candidate_skill
                    or candidate_skill in required_skill
                    for candidate_skill in candidate_skills
                ):
                    return False, []

        # Role filtering
        searchable_profile = self._profile_text(profile)

        if query.role:
            role_terms = query.role.lower().split()

            if not all(term in searchable_profile for term in role_terms):
                return False, []

        # Experience filtering
        if query.minimum_years_experience is not None:
            candidate_years = self._extract_experience_years(profile)

            if candidate_years < query.minimum_years_experience:
                return False, []

        # Keyword filtering
        if query.keywords:
            for keyword in query.keywords:
                if keyword.lower() not in searchable_profile:
                    return False, []

        # Safely retrieve evidence if supported by knowledge base
        if hasattr(self.knowledge_base, "get_candidate_evidence"):
            evidence = self.knowledge_base.get_candidate_evidence(
                candidate_id,
                " ".join(
                    query.skills
                    + query.keywords
                    + ([query.role] if query.role else [])
                ),
            )
        else:
            evidence = []

        return True, evidence

    def _profile_text(self, profile) -> str:
        """Create searchable text from a candidate profile."""

        values = []

        # Extract fields safely whether profile is an object or a dictionary
        if hasattr(profile, "skills"):
            skills = getattr(profile, "skills", []) or []
            certifications = getattr(profile, "certifications", []) or []
            experiences = getattr(profile, "experience", []) or []
            projects = getattr(profile, "projects", []) or []
            educations = getattr(profile, "education", []) or []
        elif isinstance(profile, dict):
            skills = profile.get("skills", []) or []
            certifications = profile.get("certifications", []) or []
            experiences = profile.get("experience", []) or []
            projects = profile.get("projects", []) or []
            educations = profile.get("education", []) or []
        else:
            skills, certifications, experiences, projects, educations = [], [], [], [], []

        values.extend(skills)
        values.extend(certifications)

        for experience in experiences:
            if isinstance(experience, dict):
                values.extend(str(v) for v in experience.values())
            else:
                values.extend([
                    getattr(experience, "title", "") or getattr(experience, "role", ""),
                    getattr(experience, "company", ""),
                    getattr(experience, "description", ""),
                    getattr(experience, "duration", ""),
                ])

        for project in projects:
            if isinstance(project, dict):
                values.extend(str(value) for value in project.values())
            else:
                values.append(str(project))

        for education in educations:
            if isinstance(education, dict):
                values.extend(str(v) for v in education.values())
            else:
                values.extend([
                    getattr(education, "degree", ""),
                    getattr(education, "institution", ""),
                    getattr(education, "field", ""),
                ])

        return " ".join(
            str(value).lower()
            for value in values
            if value
        )

    def search(self, question: str) -> list[dict]:
        """
        Execute a natural-language candidate search.
        """

        query = self.parse_query(question)

        results = []

        for candidate in self.knowledge_base.all_candidates():
            matches, evidence = self._candidate_matches(
                candidate,
                query,
            )

            if not matches:
                continue

            # Extract candidate_id and profile safely
            if hasattr(candidate, "profile"):
                candidate_id = getattr(candidate, "candidate_id", "")
                profile = candidate.profile
            elif isinstance(candidate, dict):
                candidate_id = candidate.get("candidate_id", "")
                profile = candidate.get("profile", {})
            else:
                candidate_id = getattr(candidate, "candidate_id", "")
                profile = candidate

            results.append({
                "candidate_id": candidate_id,
                "profile": profile,
                "matched_skills": query.skills,
                "evidence": evidence,
                "search_query": query.to_dict(),
            })

        return results