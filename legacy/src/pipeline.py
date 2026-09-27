from src.parser import ResumeParser
from src.validation import DataValidator
from src.database import CandidateDatabase
from config import DATABASE_PATH
from src.logger import logger 

class ResumePipeline:

    def __init__(self) -> None:
        """Initializes components and triggers table creation structure."""
        self.parser = ResumeParser()
        self.validator = DataValidator()
        self.database = CandidateDatabase(DATABASE_PATH)
        self.database.create_table()

    def process_resume(self, file_path: str) -> dict:
        """Process a resume file from parsing to database storage with conditional accuracy logging."""
        logger.info(f"Processing resume workflow started for: {file_path}")

        # Extract features using our optimized parser layer
        candidate_data = self.parser.parse_resume(file_path)

        # Run pipeline structural validations
        is_valid = self.validator.validate_candidate(candidate_data)
        if not is_valid:
            logger.error(f"Validation failed for candidate extraction data elements: {candidate_data}")
            raise ValueError("Candidate data failed validation.")

        # Attempt to insert records and record the operational boolean status
        was_inserted = self.database.insert_candidate(
            email=candidate_data["email"],
            phone=candidate_data["phone"],
            skills=", ".join(candidate_data["skills"])
        )

        # Log appropriate state messages matching reality
        if was_inserted:
            logger.info(f"Successfully saved new candidate record for: {candidate_data['email']}")
        else:
            logger.warning(f"Duplicate candidate skipped to protect database integrity: {candidate_data['email']}")

        return candidate_data