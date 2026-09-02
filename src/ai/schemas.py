from dataclasses import dataclass, field
from typing import List, Optional


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