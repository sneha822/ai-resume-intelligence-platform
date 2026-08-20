from typing import List, Dict


class JobMatcher:
    """Match candidate resume skills against job-description keywords."""

    def normalize_tokens(
        self,
        tokens: List[str]
    ) -> List[str]:
        """Normalize tokens for reliable comparison."""

        return [
            token.lower().strip()
            for token in tokens
            if token and token.strip()
        ]

    def find_matching_tokens(
        self,
        resume_skills: List[str],
        job_keywords: List[str]
    ) -> List[str]:
        """Return skills appearing in both the resume and JD."""

        resume_tokens = set(
            self.normalize_tokens(
                resume_skills
            )
        )

        jd_tokens = set(
            self.normalize_tokens(
                job_keywords
            )
        )

        return sorted(
            resume_tokens.intersection(
                jd_tokens
            )
        )

    def find_missing_tokens(
        self,
        resume_skills: List[str],
        job_keywords: List[str]
    ) -> List[str]:
        """Return JD requirements missing from the resume."""

        resume_tokens = set(
            self.normalize_tokens(
                resume_skills
            )
        )

        jd_tokens = set(
            self.normalize_tokens(
                job_keywords
            )
        )

        return sorted(
            jd_tokens - resume_tokens
        )

    def find_extra_tokens(
        self,
        resume_skills: List[str],
        job_keywords: List[str]
    ) -> List[str]:
        """Return resume skills not explicitly required by the JD."""

        resume_tokens = set(
            self.normalize_tokens(
                resume_skills
            )
        )

        jd_tokens = set(
            self.normalize_tokens(
                job_keywords
            )
        )

        return sorted(
            resume_tokens - jd_tokens
        )

    def match(
        self,
        resume_skills: List[str],
        job_keywords: List[str]
    ) -> Dict[str, List[str]]:
        """Generate the complete token-matching result."""

        return {
            "matched_tokens": self.find_matching_tokens(
                resume_skills,
                job_keywords
            ),
            "missing_tokens": self.find_missing_tokens(
                resume_skills,
                job_keywords
            ),
            "extra_tokens": self.find_extra_tokens(
                resume_skills,
                job_keywords
            )
        }