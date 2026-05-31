from src.storage import DataStorage

candidate_data = [
    {
        "email": "john@gmail.com",
        "phone": "9876543210",
        "skills": ["python", "sql"]
    },
    {
        "email": "jane@gmail.com",
        "phone": "9999999999",
        "skills": ["python"]
    }
]

storage = DataStorage()

storage.save_candidates(
    candidate_data,
    "data/candidates.csv"
)