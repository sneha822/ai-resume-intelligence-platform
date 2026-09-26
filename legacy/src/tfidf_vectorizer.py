import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer


class ResumeTfidfVectorizer:
    """Convert resume text into TF-IDF numerical vectors."""

    def __init__(
        self,
        max_features: int = 1000
    ) -> None:

        self.vectorizer = TfidfVectorizer(
            max_features=max_features
        )

    def fit_transform(
        self,
        documents: list
    ):
        """
        Learn vocabulary from documents and
        transform them into TF-IDF vectors.
        """

        return self.vectorizer.fit_transform(
            documents
        )

    def transform(
        self,
        documents: list
    ):
        """
        Transform new documents using the
        already learned vocabulary.
        """

        return self.vectorizer.transform(
            documents
        )

    def get_feature_names(self) -> list:
        """
        Return the vocabulary learned by TF-IDF.
        """

        return (
            self.vectorizer
            .get_feature_names_out()
            .tolist()
        )