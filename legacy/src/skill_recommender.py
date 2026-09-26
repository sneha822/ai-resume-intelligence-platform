class SkillRecommendationEngine:
    """Recommend missing skills for a target job role."""

    ROLE_SKILLS = {
        "ML Engineer": {
            "python",
            "machine learning",
            "sql",
            "docker",
            "aws"
        },

        "Data Scientist": {
            "python",
            "sql",
            "machine learning",
            "statistics",
            "pandas",
            "numpy"
        },

        "Web Developer": {
            "html",
            "css",
            "javascript",
            "react",
            "git"
        }
    }

    def get_required_skills(
        self,
        role: str
    ) -> set:
        """
        Return the required skills for a job role.
        """

        return self.ROLE_SKILLS.get(
            role,
            set()
        )

    def find_missing_skills(
        self,
        candidate_skills: list,
        role: str
    ) -> list:
        """
        Find skills required for the target role
        that are missing from the candidate profile.
        """

        candidate_skills = {
            skill.lower().strip()
            for skill in candidate_skills
        }

        required_skills = (
            self.get_required_skills(role)
        )

        missing_skills = (
            required_skills
            - candidate_skills
        )

        return sorted(
            missing_skills
        )

    def recommend_skills(
        self,
        candidate_skills: list,
        role: str
    ) -> dict:
        """
        Generate skill recommendations.
        """

        required_skills = (
            self.get_required_skills(role)
        )

        missing_skills = (
            self.find_missing_skills(
                candidate_skills,
                role
            )
        )

        return {
            "role": role,
            "required_skills": sorted(
                required_skills
            ),
            "missing_skills": missing_skills
        }