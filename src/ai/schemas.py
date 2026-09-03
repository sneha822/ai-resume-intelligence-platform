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
class CandidateEvaluation:
    overall_score: float
    fit_level: str
    strengths: list[str] = field(default_factory=list)
    skill_gaps: list[str] = field(default_factory=list)
    experience_fit: str = ""
    technical_fit: str = ""
    reasoning: str = ""

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):

        score = float(data.get("overall_score", 0))

        if score < 0 or score > 100:
            raise ValueError(
                "overall_score must be between 0 and 100."
            )

        return cls(
            overall_score=score,
            fit_level=data.get("fit_level", ""),
            strengths=data.get("strengths", []),
            skill_gaps=data.get("skill_gaps", []),
            experience_fit=data.get("experience_fit", ""),
            technical_fit=data.get("technical_fit", ""),
            reasoning=data.get("reasoning", "")
        )


@dataclass
class Experience:

    company: Optional[str] = None

    role: Optional[str] = None

    duration: Optional[str] = None

    responsibilities: List[str] = field(
        default_factory=list
    )

    achievements: List[str] = field(
        default_factory=list
    )


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

    skills: List[str] = field(
        default_factory=list
    )

    experience: List[Experience] = field(
        default_factory=list
    )

    education: List[Education] = field(
        default_factory=list
    )

    certifications: List[str] = field(
        default_factory=list
    )

    projects: List[str] = field(
        default_factory=list
    )

    def to_dict(self) -> dict:
        """Convert profile into a dictionary."""

        return asdict(self)

    @classmethod
    def from_dict(
        cls,
        data: dict
    ):
        """Create profile from dictionary."""

        experience_data = data.get(
            "experience",
            []
        )

        education_data = data.get(
            "education",
            []
        )

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
            skills=data.get(
                "skills",
                []
            ),
            experience=experience,
            education=education,
            certifications=data.get(
                "certifications",
                []
            ),
            projects=data.get(
                "projects",
                []
            )
        )