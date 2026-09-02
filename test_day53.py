from src.ai.hybrid_parser import HybridResumeParser
from src.ai.schemas import CandidateProfile


class FakeAIExtractor:

    def extract(self, resume_text):

        return CandidateProfile(
            name="John Doe",
            email="john@example.com",
            phone="9876543210",
            skills=["Python", "SQL"],
            experience=[],
            education=[],
            certifications=[],
            projects=[]
        )


class FakeFailingAIExtractor:

    def extract(self, resume_text):
        raise RuntimeError("AI service unavailable")


class FakeRuleParser:

    def parse_resume(self, file_path):

        return {
            "name": "Fallback Candidate",
            "email": "fallback@example.com"
        }


def test_ai_parser_success(tmp_path):

    resume = tmp_path / "resume.txt"

    resume.write_text(
        "John Doe\n"
        "john@example.com\n"
        "Python SQL"
    )

    parser = HybridResumeParser(
        ai_extractor=FakeAIExtractor(),
        rule_parser=FakeRuleParser()
    )

    result = parser.parse_resume(str(resume))

    assert result["name"] == "John Doe"
    assert result["email"] == "john@example.com"


def test_rule_based_fallback(tmp_path):

    resume = tmp_path / "resume.txt"

    resume.write_text(
        "Fallback Candidate\n"
        "fallback@example.com"
    )

    parser = HybridResumeParser(
        ai_extractor=FakeFailingAIExtractor(),
        rule_parser=FakeRuleParser()
    )

    result = parser.parse_resume(str(resume))

    assert result["name"] == "Fallback Candidate"
    assert result["email"] == "fallback@example.com"