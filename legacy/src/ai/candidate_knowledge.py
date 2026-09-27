from dataclasses import dataclass, field
from typing import Any


@dataclass
class CandidateRecord:
    """
    Searchable representation of a candidate.
    """

    candidate_id: str
    profile: dict[str, Any]

    def searchable_text(self) -> str:
        """
        Convert important candidate information into
        searchable text.
        """

        parts = []

        parts.extend(self.profile.get("skills", []))
        parts.extend(self.profile.get("certifications", []))

        for experience in self.profile.get("experience", []):
            if isinstance(experience, dict):
                parts.extend(
                    str(value)
                    for value in experience.values()
                )

        for project in self.profile.get("projects", []):
            if isinstance(project, dict):
                parts.extend(
                    str(value)
                    for value in project.values()
                )

        for education in self.profile.get("education", []):
            if isinstance(education, dict):
                parts.extend(
                    str(value)
                    for value in education.values()
                )

        return " ".join(parts).lower()


class CandidateKnowledgeBase:
    """
    In-memory candidate knowledge layer.

    This is intentionally simple for the first version.
    A persistent/vector-backed implementation can be added later.
    """

    def __init__(self):
        self.candidates: dict[str, CandidateRecord] = {}

    def add_candidate(
        self,
        candidate_id: str,
        profile: dict
    ):
        if not candidate_id:
            raise ValueError(
                "candidate_id cannot be empty."
            )

        if not profile:
            raise ValueError(
                "Candidate profile cannot be empty."
            )

        self.candidates[candidate_id] = CandidateRecord(
            candidate_id=candidate_id,
            profile=profile
        )

    def get_candidate(self, candidate_id: str):
        return self.candidates.get(candidate_id)

    def all_candidates(self):
        return list(self.candidates.values())

    def search(self, query: str):
        """
        Search candidates using case-insensitive
        keyword matching across their knowledge.
        """

        if not query or not query.strip():
            return []

        query = query.lower().strip()

        results = []

        for candidate in self.candidates.values():

            searchable_text = candidate.searchable_text()

            if query in searchable_text:
                results.append(candidate)

        return results

def get_candidate_evidence(self, candidate_id: str, query: str):
        """
        Extract supporting evidence for a given candidate matching the search query tokens.
        Handles both dataclass objects and raw dictionary structures.
        """
        candidate = self.get_candidate(candidate_id)
        if candidate is None:
            return []

        if not query or not query.strip():
            return []

        # Tokenize query into distinct lowercase terms
        query_tokens = [token.lower().strip() for token in query.split() if token.strip()]
        if not query_tokens:
            return []

        # Extract profile safely whether candidate is a CandidateRecord, dict, or object
        if hasattr(candidate, "profile"):
            profile = getattr(candidate, "profile")
        elif isinstance(candidate, dict):
            profile = candidate.get("profile", {})
        else:
            profile = {}

        # Safely extract core sections
        if hasattr(profile, "skills"):
            skills = getattr(profile, "skills", []) or []
            experiences = getattr(profile, "experience", []) or []
            projects = getattr(profile, "projects", []) or []
            certifications = getattr(profile, "certifications", []) or []
        elif isinstance(profile, dict):
            skills = profile.get("skills", []) or []
            experiences = profile.get("experience", []) or []
            projects = profile.get("projects", []) or []
            certifications = profile.get("certifications", []) or []
        else:
            skills, experiences, projects, certifications = [], [], [], []

        evidence = []

        # 1. Check Skills
        for skill in skills:
            skill_text = str(skill).lower()
            if any(token in skill_text or skill_text in token for token in query_tokens):
                evidence.append({"type": "skill", "content": str(skill)})

        # 2. Check Certifications
        for cert in certifications:
            cert_text = str(cert).lower()
            if any(token in cert_text for token in query_tokens):
                evidence.append({"type": "certification", "content": str(cert)})

        # 3. Check Experience
        for exp in experiences:
            if isinstance(exp, dict):
                exp_text = " ".join(str(v) for v in exp.values() if v).lower()
            else:
                title = getattr(exp, "title", "") or getattr(exp, "role", "") or ""
                company = getattr(exp, "company", "") or ""
                description = getattr(exp, "description", "") or ""
                exp_text = f"{title} {company} {description}".lower()

            if any(token in exp_text for token in query_tokens):
                evidence.append({"type": "experience", "content": exp})

        # 4. Check Projects
        for proj in projects:
            if isinstance(proj, dict):
                proj_text = " ".join(str(v) for v in proj.values() if v).lower()
            else:
                name = getattr(proj, "name", "") or getattr(proj, "title", "") or ""
                desc = getattr(proj, "description", "") or ""
                proj_text = f"{name} {desc}".lower() if (name or desc) else str(proj).lower()

            if any(token in proj_text for token in query_tokens):
                evidence.append({"type": "project", "content": proj})

        return evidence