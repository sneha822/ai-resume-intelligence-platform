import re


class ResumeFeatureExtractor:

    def extract_experience_years(
        self,
        text: str
    ) -> int:

        pattern = r"(\d+)\+?\s+years"

        matches = re.findall(
            pattern,
            text.lower()
        )

        if matches:

            return max(
                map(int, matches)
            )

        return 0

    def extract_project_count(
        self,
        text: str
    ) -> int:

        keywords = [
            "project",
            "projects"
        ]

        count = 0

        for keyword in keywords:

            count += (
                text.lower()
                .count(keyword)
            )

        return count

    def extract_certification_count(
        self,
        text: str
    ) -> int:

        keywords = [
            "certificate",
            "certification"
        ]

        count = 0

        for keyword in keywords:

            count += (
                text.lower()
                .count(keyword)
            )

        return count