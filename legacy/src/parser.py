import re
import unicodedata
from src.reader import read_resume_file
from src.logger import logger
from src.feature_extractor import ResumeFeatureExtractor


class ResumeParser:
    def __init__(self):
        # We will initialize advanced feature extractors here in Day 21
        self.feature_extractor = ResumeFeatureExtractor()

    def clean_text(self, text: str) -> str:
        """Normalizes Unicode characters and fixes standard LaTeX PDF ligatures."""
        if not text:
            return ""
        
        # Normalize special unicode fonts and symbols
        text = unicodedata.normalize("NFKD", text)
        
        # Replace common LaTeX PDF ligatures that corrupt keyword parsing
        ligature_map = {
            "ﬁ": "fi",
            "ﬂ": "fl",
            "ﬀ": "ff",
            "ﬃ": "ffi",
            "ﬄ": "ffl",
            "–": "-",
            "—": "-",
        }
        for ligature, replacement in ligature_map.items():
            text = text.replace(ligature, replacement)
            
        return text

    def extract_email(self, text: str) -> str:
        """Extracts the first email address found in the text."""
        # Added \b at the beginning
        pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not Found"

    def extract_phone(self, text: str) -> str:
        """Extracts a standard phone number configuration."""
        pattern = r'\b\d{10}\b'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not Found"

    def extract_skills(self, text: str) -> list:
        """Extracts matched keywords from a predefined skills list."""
        skills_database = ["python", "sql", "machine learning", "excel", "aws", "git"]
        found_skills = []
        
        text_lower = text.lower()
        for skill in skills_database:
            # Word boundary regex prevents partial/garbled string false positives
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
                
        return found_skills

    def parse_resume(self, file_path: str) -> dict:
        """Core pipeline method that reads the file (PDF or TXT) and extracts elements."""
        try:
            # 1. Read the file contents
            raw_text = read_resume_file(file_path)
            
            # 2. Clean ligatures and encoding noise
            cleaned_text = self.clean_text(raw_text)
            
            # 3. Extract basic schema elements
            email = self.extract_email(cleaned_text)
            phone = self.extract_phone(cleaned_text)
            skills = self.extract_skills(cleaned_text)
            
            # 4. Extract feature intelligence metrics
            experience_years = self.feature_extractor.extract_experience_years(cleaned_text)
            project_count = self.feature_extractor.extract_project_count(cleaned_text)
            certification_count = self.feature_extractor.extract_certification_count(cleaned_text)
            
            # 5. Return JSON schema
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