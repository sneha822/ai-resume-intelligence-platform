from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CandidateRecord:
    candidate_id: str
    profile: Dict[str, Any]
    relevance_score: float = 0.0

    def __getitem__(self, item):
        if item == "candidate_id":
            return self.candidate_id
        if item == "profile":
            return self.profile
        if item == "relevance_score":
            return self.relevance_score
        raise KeyError(item)


class CandidateKnowledgeBase:
    """
    Manages in-memory candidate profiles and provides multi-term search
    and granular evidence retrieval across candidate data.
    """

    def __init__(self):
        self._candidates: Dict[str, CandidateRecord] = {}

    def add_candidate(self, candidate_id: str, profile: Dict[str, Any]) -> None:
        self._candidates[candidate_id] = CandidateRecord(
            candidate_id=candidate_id,
            profile=profile
        )

    def get_candidate(self, candidate_id: str) -> Optional[CandidateRecord]:
        return self._candidates.get(candidate_id)

    def search(self, query: str) -> List[CandidateRecord]:
        query_terms = [term.lower() for term in query.split() if term.strip()]
        if not query_terms:
            return []

        results = []
        for candidate in self._candidates.values():
            profile = candidate.profile
            searchable_parts = []

            if profile.get("name"):
                searchable_parts.append(str(profile["name"]))

            searchable_parts.extend(profile.get("skills", []))

            for exp in profile.get("experience", []):
                searchable_parts.extend([
                    exp.get("company", ""),
                    exp.get("role", ""),
                    exp.get("duration", "")
                ])

            for proj in profile.get("projects", []):
                searchable_parts.append(proj.get("name", ""))
                searchable_parts.extend(proj.get("technologies", []))

            searchable_parts.extend(profile.get("certifications", []))

            searchable_text = " ".join(filter(None, searchable_parts)).lower()

            matched_terms = sum(1 for term in query_terms if term in searchable_text)

            if matched_terms == len(query_terms):
                candidate.relevance_score = 100.0
                results.append(candidate)

        return results

    def get_candidate_evidence(self, candidate_id: str, term: str) -> List[Dict[str, Any]]:
        candidate = self.get_candidate(candidate_id)
        if not candidate:
            return []

        term_lower = term.lower()
        profile = candidate.profile
        evidence_items = []

        for skill in profile.get("skills", []):
            if term_lower in skill.lower():
                evidence_items.append({
                    "type": "skill",
                    "value": skill
                })

        for exp in profile.get("experience", []):
            exp_str = f"{exp.get('role', '')} at {exp.get('company', '')}"
            if term_lower in exp_str.lower():
                evidence_items.append({
                    "type": "experience",
                    "value": exp
                })

        for proj in profile.get("projects", []):
            techs = [t.lower() for t in proj.get("technologies", [])]
            if term_lower in proj.get("name", "").lower() or term_lower in techs:
                evidence_items.append({
                    "type": "project",
                    "value": proj
                })

        for cert in profile.get("certifications", []):
            if term_lower in cert.lower():
                evidence_items.append({
                    "type": "certification",
                    "value": cert
                })

        return evidence_items