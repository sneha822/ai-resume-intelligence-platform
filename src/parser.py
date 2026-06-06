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
        # 1. Read the original raw text
        raw_text = read_text_file(file_path)

        # 2. Extract email and phone from RAW text so symbols (@, .) aren't lost!
        email = self.extractor.extract_email(raw_text)
        phone = self.extractor.extract_phone(raw_text)

        # 3. Clean the text ONLY for skills extraction
        cleaned_text = self.cleaner.clean_text(raw_text)
        skills = self.extractor.extract_skills(cleaned_text)

        return {
            "email": email,
            "phone": phone,
            "skills": skills
        }