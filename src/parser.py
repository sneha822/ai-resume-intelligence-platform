from src.reader import read_text_file
from src.preprocessing import ResumeCleaner
from src.extraction import SkillExtractor


class ResumeParser:
    """
    Main resume parser.
    """

    def __init__(self):

        self.cleaner = ResumeCleaner()

        self.extractor = SkillExtractor()

    def parse_resume(self, file_path: str) -> dict:

        raw_text = read_text_file(file_path)

        cleaned_text = self.cleaner.clean_text(raw_text)

        email = self.extractor.extract_email(cleaned_text)

        phone = self.extractor.extract_phone(cleaned_text)

        skills = self.extractor.extract_skills(cleaned_text)

        return {
            "email": email,
            "phone": phone,
            "skills": skills
        }