import re
from src.reader import read_resume_file
from src.logger import logger

class ResumeParser:
    def __init__(self):
        # We will initialize advanced feature extractors here in Day 21
        pass

    def extract_email(self, text: str) -> str:
        """Extracts the first email address found in the text."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not Found"

    def extract_phone(self, text: str) -> str:
        """Extracts a standard phone number configuration."""
        pattern = r'\b\d{10}\b'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not Found"

    def extract_skills(self, text: str) -> list:
        """Extracts matched keywords from a predefined skills list."""
        # A simple baseline list of skills to match against
        skills_database = ["python", "sql", "machine learning", "excel", "aws", "git"]
        found_skills = []
        
        text_lower = text.lower()
        for skill in skills_database:
            if skill in text_lower:
                found_skills.append(skill)
                
        return found_skills

    def parse_resume(self, file_path: str) -> dict:
        """Core pipeline method that reads the file (PDF or TXT) and extracts elements."""
        try:
            # Step 3 Swap: Using the hybrid reader capable of handling both TXT and PDF formats
            raw_text = read_resume_file(file_path)
            
            # Extract basic schema elements
            email = self.extract_email(raw_text)
            phone = self.extract_phone(raw_text)
            skills = self.extract_skills(raw_text)
            
            # Formulate structural JSON schema response
            return {
                "email": email,
                "phone": phone,
                "skills": skills
            }
            
        except Exception as error:
            logger.error(f"Error encountered during resume parsing execution: {str(error)}")
            raise