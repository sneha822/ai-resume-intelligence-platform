from typing import List


class JobDescriptionParser:
    """Parse and extract relevant keywords from job descriptions."""

    def __init__(self) -> None:
        self.skill_database = {
            "python",
            "sql",
            "machine learning",
            "deep learning",
            "java",
            "c++",
            "c",
            "docker",
            "aws",
            "azure",
            "gcp",
            "flask",
            "fastapi",
            "streamlit",
            "pandas",
            "numpy",
            "scikit-learn",
            "tensorflow",
            "pytorch",
            "git",
            "github",
            "nlp",
            "computer vision",
            "data analysis",
            "data science",
            "react",
            "javascript",
            "html",
            "css",
        }

    def clean_text(
        self,
        text: str
    ) -> str:
        """Normalize job description text."""

        return (
            text
            .lower()
            .replace("\n", " ")
            .strip()
        )

    def extract_keywords(
        self,
        text: str
    ) -> List[str]:
        """Extract known technical skills from job description."""

        cleaned_text = self.clean_text(
            text
        )

        found_skills = []

        for skill in self.skill_database:

            if skill in cleaned_text:
                found_skills.append(
                    skill
                )

        return sorted(
            found_skills
        )

    def parse_job_description(
        self,
        text: str
    ) -> dict:
        """Return structured job description data."""

        cleaned_text = self.clean_text(
            text
        )

        keywords = self.extract_keywords(
            cleaned_text
        )

        return {
            "cleaned_text": cleaned_text,
            "keywords": keywords,
        }