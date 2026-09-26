from typing import Dict, List


class MatchExplainer:
    """Explain resume-to-JD matching results."""

    def explain_match(
        self,
        matched_tokens: List[str],
        missing_tokens: List[str],
        extra_tokens: List[str],
        match_score: float
    ) -> Dict:

        total_required = (
            len(matched_tokens)
            + len(missing_tokens)
        )

        if total_required > 0:
            matched_percentage = round(
                (
                    len(matched_tokens)
                    / total_required
                ) * 100,
                2
            )
        else:
            matched_percentage = 0.0

        return {
            "match_score": match_score,
            "total_required_skills": total_required,
            "matched_count": len(
                matched_tokens
            ),
            "missing_count": len(
                missing_tokens
            ),
            "extra_count": len(
                extra_tokens
            ),
            "matched_percentage": (
                matched_percentage
            ),
            "matched_tokens": matched_tokens,
            "missing_tokens": missing_tokens,
            "extra_tokens": extra_tokens
        }

    def generate_summary(
        self,
        explanation: Dict
    ) -> str:
        """Generate a human-readable explanation."""

        score = explanation[
            "match_score"
        ]

        matched = explanation[
            "matched_count"
        ]

        missing = explanation[
            "missing_count"
        ]

        if score >= 80:
            assessment = (
                "Strong match for this job description."
            )

        elif score >= 50:
            assessment = (
                "Moderate match with some "
                "requirements still missing."
            )

        else:
            assessment = (
                "Low match. Several job "
                "requirements are missing."
            )

        return (
            f"The candidate matches {matched} "
            f"required skill(s) with a match score "
            f"of {score}%. "
            f"There are {missing} missing "
            f"requirement(s). "
            f"{assessment}"
        )