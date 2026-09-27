from dataclasses import (
    asdict,
    dataclass,
    field
)
from typing import (
    List,
    Optional
)


@dataclass
class EvidenceItem:
    claim: str
    evidence: str
    category: str = ""

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, cls):
            return data
        if not isinstance(data, dict):
            return cls(claim="", evidence="", category="")
        return cls(
            claim=data.get("claim", ""),
            evidence=data.get("evidence", ""),
            category=data.get("category", "")
        )


@dataclass
class CandidateEvaluation:
    overall_score: float
    fit_level: str

    strengths: list[str] = field(default_factory=list)
    skill_gaps: list[str] = field(default_factory=list)

    strength_evidence: list[EvidenceItem] = field(
        default_factory=list
    )

    gap_evidence: list[EvidenceItem] = field(
        default_factory=list
    )

    experience_fit: str = ""
    technical_fit: str = ""
    reasoning: str = ""

    def to_dict(self):
        return {
            "overall_score": self.overall_score,
            "fit_level": self.fit_level,
            "strengths": self.strengths,
            "skill_gaps": self.skill_gaps,
            "strength_evidence": [
                item.to_dict() if hasattr(item, "to_dict") else item
                for item in self.strength_evidence
            ],
            "gap_evidence": [
                item.to_dict() if hasattr(item, "to_dict") else item
                for item in self.gap_evidence
            ],
            "experience_fit": self.experience_fit,
            "technical_fit": self.technical_fit,
            "reasoning": self.reasoning
        }

    @classmethod
    def from_dict(cls, data):
        score = float(data.get("overall_score", 0))

        if score < 0 or score > 100:
            raise ValueError(
                "overall_score must be between 0 and 100."
            )

        strength_evidence = [
            EvidenceItem.from_dict(item)
            for item in data.get("strength_evidence", [])
        ]

        gap_evidence = [
            EvidenceItem.from_dict(item)
            for item in data.get("gap_evidence", [])
        ]

        return cls(
            overall_score=score,
            fit_level=data.get("fit_level", ""),
            strengths=data.get("strengths", []),
            skill_gaps=data.get("skill_gaps", []),
            strength_evidence=strength_evidence,
            gap_evidence=gap_evidence,
            experience_fit=data.get("experience_fit", ""),
            technical_fit=data.get("technical_fit", ""),
            reasoning=data.get("reasoning", "")
        )


@dataclass
class Experience:
    company: Optional[str] = None
    role: Optional[str] = None
    title: Optional[str] = None  # Added for compatibility
    duration: Optional[str] = None
    description: Optional[str] = None  # Added for compatibility
    responsibilities: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Normalize role/title
        if not self.role and self.title:
            self.role = self.title
        elif not self.title and self.role:
            self.title = self.role
            
        # Normalize description into responsibilities if responsibilities is empty
        if self.description and not self.responsibilities:
            self.responsibilities = [self.description]


@dataclass
class Education:
    degree: Optional[str] = None
    field: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[str] = None


@dataclass
class CandidateProfile:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert profile into a dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        """Create profile from dictionary."""
        experience_data = data.get("experience", [])
        education_data = data.get("education", [])

        experience = [
            Experience(**item)
            for item in experience_data
            if isinstance(item, dict)
        ]

        education = [
            Education(**item)
            for item in education_data
            if isinstance(item, dict)
        ]

        return cls(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            skills=data.get("skills", []),
            experience=experience,
            education=education,
            certifications=data.get("certifications", []),
            projects=data.get("projects", [])
        )


@dataclass
class CandidateSearchQuery:
    """Structured representation of a recruiter search query."""

    skills: list[str] = field(default_factory=list)
    role: Optional[str] = None
    minimum_years_experience: Optional[float] = None
    keywords: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "skills": self.skills,
            "role": self.role,
            "minimum_years_experience": self.minimum_years_experience,
            "keywords": self.keywords,
        }

    @classmethod
    def from_dict(cls, data: dict):
        if not isinstance(data, dict):
            raise ValueError("Search query must be a dictionary.")

        skills = data.get("skills") or data.get("required_skills", [])
        keywords = data.get("keywords", [])
        role = data.get("role") or (data.get("job_titles")[0] if data.get("job_titles") else None)
        minimum_years = data.get("minimum_years_experience") or data.get("min_years_experience")

        if not isinstance(skills, list):
            raise ValueError("skills must be a list.")

        if not isinstance(keywords, list):
            raise ValueError("keywords must be a list.")

        if role is not None and not isinstance(role, str):
            raise ValueError("role must be a string or None.")

        if minimum_years is not None:
            try:
                minimum_years = float(minimum_years)
            except (TypeError, ValueError):
                raise ValueError(
                    "minimum_years_experience must be numeric."
                )

            if minimum_years < 0:
                raise ValueError(
                    "minimum_years_experience cannot be negative."
                )

        return cls(
            skills=[str(skill).strip().lower() for skill in skills if str(skill).strip()],
            role=role.strip().lower() if role else None,
            minimum_years_experience=minimum_years,
            keywords=[
                str(keyword).strip().lower()
                for keyword in keywords
                if str(keyword).strip()
            ],
        )