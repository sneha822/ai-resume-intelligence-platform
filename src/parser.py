import re
from src.reader import read_resume_file
from src.logger import logger
from src.feature_extractor import (
    ResumeFeatureExtractor
)


class ResumeParser:
    def __init__(self):
        # We will initialize advanced feature extractors here in Day 21
        pass
        self.feature_extractor = ResumeFeatureExtractor()

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
            # 1. Read the file contents (From your Mini Day 20.5 setup)
            raw_text = read_resume_file(file_path)
            
            # 2. Extract basic schema elements
            email = self.extract_email(raw_text)
            phone = self.extract_phone(raw_text)
            skills = self.extract_skills(raw_text)
            
            # 3. ADD THE NEW INTELLIGENCE METRICS HERE (Day 21):
            experience_years = self.feature_extractor.extract_experience_years(raw_text)
            project_count = self.feature_extractor.extract_project_count(raw_text)
            certification_count = self.feature_extractor.extract_certification_count(raw_text)
            
            # 4. Update the return dictionary to include the new metrics
            return {
                "email": email,
                "phone": phone,
                "skills": skills,
                "experience_years": experience_years,
                "project_count": project_count,
                "certification_count": certification_count
            }
            
        except Exception as error:
            logger.error(f"Error encountered during resume parsing execution: {str(error)}")
            raise