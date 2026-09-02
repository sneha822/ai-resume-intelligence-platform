from src.ai.schemas import (
    CandidateProfile
)


def main():

    print(
        "=== DAY 52 SCHEMA TEST ==="
    )

    data = {
        "name": "Test Candidate",
        "email": "test@example.com",
        "phone": "9876543210",
        "skills": [
            "Python",
            "SQL"
        ],
        "experience": [],
        "education": [],
        "certifications": [],
        "projects": []
    }

    profile = (
        CandidateProfile.from_dict(
            data
        )
    )

    assert profile.name == (
        "Test Candidate"
    )

    assert profile.email == (
        "test@example.com"
    )

    assert profile.skills == [
        "Python",
        "SQL"
    ]

    print(
        "✓ Dictionary → CandidateProfile"
    )

    print(
        "✓ Schema conversion successful"
    )

    print(
        "\n=== SCHEMA TEST PASSED ==="
    )


if __name__ == "__main__":
    main()