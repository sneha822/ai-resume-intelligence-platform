import os
# Import the clean config path variable directly
from config import DATABASE_PATH
from src.database import CandidateDatabase

# Ensure the data directory exists so SQLite doesn't throw a crash error
os.makedirs(
    os.path.dirname(DATABASE_PATH), 
    exist_ok=True
)

# Initialize the database object using the clean path variable
database = CandidateDatabase(
    DATABASE_PATH
)
database.create_table()

# Test the insert operation
database.insert_candidate(
    email="johndoe@gmail.com", 
    phone="9876543210", 
    skills="python, sql"
)
print("Candidate inserted successfully")

# Test fetching and printing records out cleanly
candidates = database.fetch_all_candidates()
print("\n--- Current Candidates in Database ---")
print(candidates)