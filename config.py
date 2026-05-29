import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

LOG_DIR = os.path.join(
    BASE_DIR,
    "logs"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

ARTIFACT_DIR = os.path.join(
    BASE_DIR,
    "artifacts"
)