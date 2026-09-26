from src.job_description import (
    JobDescriptionParser
)


JD_PATH = (
    "data/job_descriptions/"
    "python_data_engineer.txt"
)


def read_job_description(
    file_path: str
) -> str:
    """Read job description from a text file."""

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


def main() -> None:

    print(
        "=== DAY 41: JD PARSING ==="
    )

    job_description = (
        read_job_description(
            JD_PATH
        )
    )

    parser = JobDescriptionParser()

    result = (
        parser.parse_job_description(
            job_description
        )
    )

    print(
        "\n--- Cleaned Job Description ---"
    )

    print(
        result["cleaned_text"]
    )

    print(
        "\n--- Extracted Keywords ---"
    )

    for keyword in result["keywords"]:

        print(
            f"- {keyword}"
        )

    print(
        "\n=== JD PARSING COMPLETE ==="
    )


if __name__ == "__main__":
    main()