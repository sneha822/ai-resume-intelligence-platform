from config import USE_AI_PARSER
from src.ai.resume_extractor import AIResumeExtractor
from src.parser import ResumeParser
from src.reader import read_resume_file


class HybridResumeParser:
    """
    Hybrid resume parser.

    Uses AI extraction when enabled.
    Falls back to the existing rule-based parser when
    AI extraction is disabled or fails.
    """

    def __init__(self, ai_extractor=None, rule_parser=None):
        self.ai_extractor = ai_extractor or AIResumeExtractor()
        self.rule_parser = rule_parser or ResumeParser()

    def _normalize_profile(self, profile):
        """Standardize parser output to a dictionary format."""
        if hasattr(profile, "to_dict"):
            return profile.to_dict()

        if isinstance(profile, dict):
            return profile

        raise TypeError("Unsupported parser output format.")

    def parse_resume(self, file_path):
        """
        Parse a resume using the configured parsing strategy.
        """
        if not USE_AI_PARSER:
            return self.rule_parser.parse_resume(file_path)

        try:
            resume_text = read_resume_file(file_path)

            if not resume_text.strip():
                raise ValueError("Resume contains no readable text.")

            profile = self.ai_extractor.extract(resume_text)

            if profile is not None:
                return self._normalize_profile(profile)

        except Exception as error:
            print(f"AI parser failed: {error}")
            print("Falling back to rule-based parser.")

        return self.rule_parser.parse_resume(file_path)