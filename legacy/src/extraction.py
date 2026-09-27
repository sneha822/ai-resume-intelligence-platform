import re


SKILLS_DATABASE = [
    "python",
    "sql",
    "machine learning",
    "java",
    "c++"
]


class SkillExtractor:
    """
    Extract information from resumes.
    """

    def extract_email(self, text: str):

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return None

    def extract_phone(self, text: str):

        pattern = r"\d{10}"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return None

    def extract_skills(self, text: str) -> list:

        found_skills = []

        for skill in SKILLS_DATABASE:

            if skill in text:
                found_skills.append(skill)

        return found_skills