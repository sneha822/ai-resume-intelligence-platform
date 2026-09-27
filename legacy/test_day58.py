from src.ai.candidate_search import NaturalLanguageCandidateSearch
from src.ai.candidate_knowledge import CandidateKnowledgeBase
from src.ai.schemas import (
    CandidateProfile,
    Experience,
    Education,
)


class FakeLLM:
    def generate(self, prompt, system_prompt=None):

        return """
        {
            "skills": ["python", "aws"],
            "role": "backend developer",
            "minimum_years_experience": 3,
            "keywords": []
        }
        """


def build_candidate():
    return CandidateProfile(
        name="John Doe",
        email="john@example.com",
        phone="1234567890",
        skills=["Python", "AWS", "FastAPI"],
        experience=[
            Experience(
                title="Backend Developer",
                company="ABC Technologies",
                duration="3 years",
                description="Built scalable backend APIs."
            )
        ],
        education=[
            Education(
                degree="B.Tech",
                institution="XYZ University",
                field="Computer Science"
            )
        ],
        certifications=[],
        projects=[
            {
                "name": "Customer Analytics Platform",
                "description": "Backend platform using Python and AWS."
            }
        ],
    )


def test_parse_natural_language_query():

    knowledge_base = CandidateKnowledgeBase()

    search_engine = NaturalLanguageCandidateSearch(
        knowledge_base,
        llm_client=FakeLLM(),
    )

    query = search_engine.parse_query(
        "Find Python and AWS backend developers with at least 3 years of experience."
    )

    assert "python" in query.skills
    assert "aws" in query.skills
    assert query.role == "backend developer"
    assert query.minimum_years_experience == 3


def test_candidate_search():

    knowledge_base = CandidateKnowledgeBase()

    knowledge_base.add_candidate(
        "candidate_001",
        build_candidate(),
    )

    search_engine = NaturalLanguageCandidateSearch(
        knowledge_base,
        llm_client=FakeLLM(),
    )

    results = search_engine.search(
        "Find Python and AWS backend developers with at least 3 years of experience."
    )

    assert len(results) == 1
    assert results[0]["candidate_id"] == "candidate_001"