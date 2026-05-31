VALID_SKILLS = {
    "python",
    "sql",
    "machine learning",
    "java",
    "c++"
}


class DataValidator:

    def has_email(self, email):

        return email is not None

    def has_valid_skills(self, skills):

        for skill in skills:

            if skill not in VALID_SKILLS:
                return False

        return True