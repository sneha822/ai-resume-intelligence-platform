import pandas as pd

# Industry-standard baseline skills for verification
VALID_SKILLS = {"python", "sql", "machine learning", "java", "c++"}


class DataValidator:

    def has_email(
        self, 
        email: str
    ) -> bool:
        """Checks if an email is present and not just empty whitespace."""
        return email is not None and str(email).strip() != ""

    def has_valid_skills(
        self, 
        skills: list
    ) -> bool:
        """Validates if the parsed skills exist within our allowed skills database."""
        if not skills:
            return False

        for skill in skills:
            if skill not in VALID_SKILLS:
                return False
        return True

    def has_duplicate_emails(
        self, 
        dataframe: pd.DataFrame
    ) -> bool:
        """
        Scans the DataFrame to detect if any candidate emails are duplicated.
        Returns True if duplicates exist, False otherwise.
        """
        return dataframe["email"].duplicated().any()