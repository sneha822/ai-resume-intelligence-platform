from config import DATABASE_PATH
from src.database import CandidateDatabase

database = CandidateDatabase(
    DATABASE_PATH
)

for candidate in database.fetch_all_candidates():

    print(candidate)