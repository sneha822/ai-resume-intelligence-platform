import re

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


class NLPPreprocessor:
    """Prepare resume text for NLP processing."""

    def __init__(self):
        self.stop_words = set(
            stopwords.words("english")
        )

        self.lemmatizer = WordNetLemmatizer()

    def clean_text(
        self,
        text: str
    ) -> str:
        """
        Remove unwanted characters and normalize text.
        """

        text = text.lower()

        text = re.sub(
            r"[^a-z\s]",
            " ",
            text
        )

        text = " ".join(
            text.split()
        )

        return text

    def tokenize(
        self,
        text: str
    ) -> list:
        """
        Convert cleaned text into tokens.
        """

        return word_tokenize(
            text
        )

    def remove_stopwords(
        self,
        tokens: list
    ) -> list:
        """
        Remove common English stopwords.
        """

        return [
            token
            for token in tokens
            if token not in self.stop_words
        ]

    def lemmatize(
        self,
        tokens: list
    ) -> list:
        """
        Convert words to their base form.
        """

        return [
            self.lemmatizer.lemmatize(
                token
            )
            for token in tokens
        ]

    def preprocess(
        self,
        text: str
    ) -> str:
        """
        Run the complete NLP preprocessing pipeline.
        """

        cleaned_text = self.clean_text(
            text
        )

        tokens = self.tokenize(
            cleaned_text
        )

        tokens = self.remove_stopwords(
            tokens
        )

        tokens = self.lemmatize(
            tokens
        )

        return " ".join(
            tokens
        )