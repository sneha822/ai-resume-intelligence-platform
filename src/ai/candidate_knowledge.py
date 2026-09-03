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

def get_candidate_evidence(
    self,
    candidate_id: str,
    query: str
):
    candidate = self.get_candidate(candidate_id)

    if candidate is None:
        return []

    query_tokens = query.lower().split()

    evidence = []

    profile = candidate.profile

    for skill in profile.get("skills", []):

        skill_text = str(skill).lower()

        if any(
            token in skill_text
            for token in query_tokens
        ):
            evidence.append({
                "type": "skill",
                "content": skill
            })

    for experience in profile.get(
        "experience",
        []
    ):

        if not isinstance(experience, dict):
            continue

        text = " ".join(
            str(value)
            for value in experience.values()
        )

        if any(
            token in text.lower()
            for token in query_tokens
        ):
            evidence.append({
                "type": "experience",
                "content": experience
            })

    for project in profile.get(
        "projects",
        []
    ):

        if not isinstance(project, dict):
            continue

        text = " ".join(
            str(value)
            for value in project.values()
        )

        if any(
            token in text.lower()
            for token in query_tokens
        ):
            evidence.append({
                "type": "project",
                "content": project
            })

    return evidence