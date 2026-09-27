import pandas as pd

# Industry-standard baseline skills for verification
VALID_SKILLS = {"python", "sql", "machine learning", "java", "c++"}


class DataValidator:

    def has_email(self, email: str) -> bool:
        """Checks if an email is present and not just empty whitespace."""
        return email is not None and str(email).strip() != ""

    def has_valid_skills(self, skills: list) -> bool:
        """Validates if the parsed skills exist within our allowed skills database (case-insensitive)."""
        if not skills:
            return False

        for skill in skills:
            # New improvement: Lowercase and strip whitespace to ensure robust matching
            clean_skill = str(skill).strip().lower()
            if clean_skill not in VALID_SKILLS:
                return False
        return True

    def validate_candidate(self, candidate_data: dict) -> bool:
        """
        NEW METHOD: Validates a single candidate dictionary before database insertion.
        Required for the Day 11 automated pipeline.
        """
        email_valid = self.has_email(candidate_data.get("email"))
        skills_valid = self.has_valid_skills(candidate_data.get("skills", []))
        
        return email_valid and skills_valid

    def has_duplicate_emails(self, dataframe: pd.DataFrame) -> bool:
        """
        Scans the DataFrame to detect if any candidate emails are duplicated.
        Returns True if duplicates exist, False otherwise.
        """
        return dataframe["email"].duplicated().any()