import string


def to_lower_case(text: str) -> str:
    """
    Convert text to lowercase.
    """

    if not isinstance(text, str):
        raise TypeError("text must be string")

    return text.lower()


def remove_punctuation(text: str) -> str:
    """
    Remove punctuation characters.
    """

    if not isinstance(text, str):
        raise TypeError("text must be string")

    return text.translate(
        str.maketrans("", "", string.punctuation)
    )


def clean_whitespace(text: str) -> str:
    """
    Remove extra spaces.
    """

    if not isinstance(text, str):
        raise TypeError("text must be string")

    return " ".join(text.split())