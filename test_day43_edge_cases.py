from src.match_scorer import MatchScorer


def main() -> None:

    scorer = MatchScorer()

    # Case 1: Perfect match
    score = scorer.calculate_match_score(
        ["python", "sql"],
        ["python", "sql"]
    )

    assert score == 100.0

    # Case 2: Partial match
    score = scorer.calculate_match_score(
        ["python"],
        ["python", "sql"]
    )

    assert score == 50.0

    # Case 3: No match
    score = scorer.calculate_match_score(
        [],
        ["python", "sql"]
    )

    assert score == 0.0

    # Case 4: Empty JD
    score = scorer.calculate_match_score(
        ["python"],
        []
    )

    assert score == 0.0

    print(
        "All Day 43 edge cases passed."
    )


if __name__ == "__main__":
    main()