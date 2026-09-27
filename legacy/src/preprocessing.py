from src.utils import (
    to_lower_case,
    remove_punctuation,
    clean_whitespace
)


class ResumeCleaner:
    """
    Clean raw resume text.
    """

    def clean_text(self, text: str) -> str:

        text = to_lower_case(text)

        text = remove_punctuation(text)

        text = clean_whitespace(text)

        return text