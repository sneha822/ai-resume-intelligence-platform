from src.ai.llm_client import LLMClient
from src.ai.schemas import (
    CandidateProfile,
    Experience,
    Education
)


def main():

    print(
        "=== DAY 51: AI INFRASTRUCTURE TEST ==="
    )

    # ==========================================
    # Test 1 — LLM Client Configuration
    # ==========================================

    client = LLMClient()

    assert client.provider
    assert client.model

    print(
        f"Provider: {client.provider}"
    )

    print(
        f"Model: {client.model}"
    )

    # ==========================================
    # Test 2 — Candidate Schema
    # ==========================================

    profile = CandidateProfile(
        name="Test Candidate",
        email="test@example.com",
        skills=[
            "Python",
            "SQL",
            "Machine Learning"
        ],
        experience=[
            Experience(
                company="Test Corp",
                role="ML Engineer",
                duration="2 years",
                achievements=[
                    "Reduced model latency by 30%"
                ]
            )
        ],
        education=[
            Education(
                degree="B.Tech",
                field="Computer Science",
                institution="Test University"
            )
        ]
    )

    assert profile.name == "Test Candidate"
    assert len(profile.skills) == 3
    assert len(profile.experience) == 1
    assert len(profile.education) == 1

    print(
        "Candidate schema: PASS"
    )

    print(
        "\n=== DAY 51 COMPLETE ==="
    )


if __name__ == "__main__":
    main()