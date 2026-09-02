from src.ai.resume_extractor import (
    AIResumeExtractor
)


SAMPLE_RESUME = """
John Doe

Email: john.doe@example.com
Phone: 9876543210

SUMMARY

Software Engineer with 3 years of experience
building Python backend applications.

SKILLS

Python
SQL
Docker
AWS
Machine Learning

EXPERIENCE

Software Engineer
ABC Technologies
2023 - Present

Built REST APIs using Python and FastAPI.
Improved API response time by 35%.
Worked with PostgreSQL and Docker.

PROJECTS

Customer Analytics Platform

Built a machine learning pipeline for customer
segmentation.

EDUCATION

B.Tech in Computer Science
XYZ University
2023

CERTIFICATIONS

AWS Certified Cloud Practitioner
"""


def main():

    print(
        "=== DAY 52: STRUCTURED AI EXTRACTION ==="
    )

    extractor = AIResumeExtractor()

    profile = extractor.extract(
        SAMPLE_RESUME
    )

    print(
        "\n--- CANDIDATE PROFILE ---"
    )

    print(
        profile.to_dict()
    )

    # --------------------------------------
    # Basic validation
    # --------------------------------------

    assert profile.name

    assert profile.email

    assert len(
        profile.skills
    ) > 0

    assert len(
        profile.experience
    ) > 0

    assert len(
        profile.education
    ) > 0

    assert len(
        profile.projects
    ) > 0

    assert len(
        profile.certifications
    ) > 0

    print(
        "\n✓ Name extracted"
    )

    print(
        "✓ Email extracted"
    )

    print(
        "✓ Skills extracted"
    )

    print(
        "✓ Experience extracted"
    )

    print(
        "✓ Education extracted"
    )

    print(
        "✓ Projects extracted"
    )

    print(
        "✓ Certifications extracted"
    )

    print(
        "\n=== DAY 52 COMPLETE ==="
    )


if __name__ == "__main__":
    main()