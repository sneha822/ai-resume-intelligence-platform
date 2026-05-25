import re

from src.reader import read_text_file


class ResumeCleaner:

    def clean_text(self, text):

        text = text.lower()

        text = text.strip()

        return text


class SkillExtractor:

    def extract_email(self, text):

        pattern = r'\S+@\S+'

        match = re.search(pattern, text)

        if match:

            return match.group()

        return None

    def extract_phone(self, text):

        pattern = r'\d{10}'

        match = re.search(pattern, text)

        if match:

            return match.group()

        return None

    def extract_skills(self, text):

        skills_database = [
            "python",
            "sql",
            "machine learning",
            "java",
            "c++"
        ]

        found_skills = []

        for skill in skills_database:

            if skill in text:

                found_skills.append(skill)

        return found_skills


class ResumeParser:

    def __init__(self):

        self.cleaner = ResumeCleaner()

        self.extractor = SkillExtractor()

    def parse_resume(self, file_path):

        raw_text = read_text_file(file_path)

        print("RAW TEXT:")
        print(raw_text)

        cleaned_text = self.cleaner.clean_text(raw_text)

        print("CLEANED TEXT:")
        print(cleaned_text)

        email = self.extractor.extract_email(cleaned_text)

        phone = self.extractor.extract_phone(cleaned_text)

        skills = self.extractor.extract_skills(cleaned_text)

        return {
            "email": email,
            "phone": phone,
            "skills": skills
        }