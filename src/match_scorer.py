from typing import List, Dict


class MatchScorer:
    """Calculate resume-to-job-description similarity scores."""

    def calculate_match_score(
        self,
        matched_tokens: List[str],
        job_keywords: List[str]
    ) -> float:
        """
        Calculate the percentage of JD keywords
        matched by the candidate.
        """

        if not job_keywords:
            return 0.0

        matched_count = len(
            set(matched_tokens)
        )

        required_count = len(
            set(job_keywords)
        )

        score = (
            matched_count
            / required_count
        ) * 100

        return round(
            score,
            2
        )

    def calculate_similarity(
        self,
        matched_tokens: List[str],
        resume_skills: List[str],
        job_keywords: List[str]
    ) -> float:
        """
        Calculate Jaccard-style similarity between
        resume skills and JD keywords.
        """

        resume_set = set(
            skill.lower().strip()
            for skill in resume_skills
        )

        jd_set = set(
            keyword.lower().strip()
            for keyword in job_keywords
        )

        if not resume_set and not jd_set:
            return 0.0

        union = (
            resume_set | jd_set
        )

        intersection = (
            resume_set & jd_set
        )

        similarity = (
            len(intersection)
            / len(union)
        ) * 100

        return round(
            similarity,
            2
        )

    def generate_score_report(
        self,
        resume_skills: List[str],
        job_keywords: List[str],
        matched_tokens: List[str]
    ) -> Dict[str, float]:
        """Generate both matching and similarity scores."""

        match_score = (
            self.calculate_match_score(
                matched_tokens,
                job_keywords
            )
        )

        similarity_score = (
            self.calculate_similarity(
                matched_tokens,
                resume_skills,
                job_keywords
            )
        )

        return {
            "match_score": match_score,
            "similarity_score": similarity_score
        }