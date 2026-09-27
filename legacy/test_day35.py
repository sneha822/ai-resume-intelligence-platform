from src.nlp_preprocessor import (
    NLPPreprocessor
)

from src.tfidf_vectorizer import (
    ResumeTfidfVectorizer
)
from src.reader import read_text_file


preprocessor = NLPPreprocessor()

documents = [
    """
    Python developer with machine learning
    and SQL experience.
    """,

    """
    Data scientist experienced in Python,
    machine learning and statistics.
    """,

    """
    Java developer working on web applications
    and backend systems.
    """
]


processed_documents = []

for document in documents:

    processed_text = (
        preprocessor.preprocess(
            document
        )
    )

    processed_documents.append(
        processed_text
    )


print("=== PROCESSED DOCUMENTS ===")

for document in processed_documents:
    print(document)


vectorizer = ResumeTfidfVectorizer()

tfidf_matrix = (
    vectorizer.fit_transform(
        processed_documents
    )
)


print("\n=== TF-IDF MATRIX ===")

print(
    tfidf_matrix.toarray()
)


print("\n=== VOCABULARY ===")

print(
    vectorizer.get_feature_names()
)


print("\n=== MATRIX SHAPE ===")

print(
    tfidf_matrix.shape
)

resume_text = read_text_file(
    "data/raw/sample_resume.txt"
)

processed_resume = (
    preprocessor.preprocess(
        resume_text
    )
)

print(
    "\n=== PROCESSED SAMPLE RESUME ==="
)

print(
    processed_resume
)