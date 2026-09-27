import pandas as pd


class SkillAnalyzer:

    def skill_frequency(
        self,
        dataframe: pd.DataFrame
    ):

        skills_count = {}

        for skills in dataframe["skills"]:

            skills = (
                str(skills)
                .replace("[", "")
                .replace("]", "")
                .replace("'", "")
            )

            skills_list = skills.split(",")

            for skill in skills_list:

                skill = skill.strip()

                if skill:

                    skills_count[skill] = (
                        skills_count.get(skill, 0)
                        + 1
                    )

        return skills_count