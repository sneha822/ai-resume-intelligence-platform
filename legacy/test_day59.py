import pytest
from typing import Any, List
from src.ai.v2_pipeline import V2RecruitingPipeline


# --- MOCK / FAKE CLASSES FOR TESTING ---

class FakeParser:
    def parse_resume(self, file_path: str) -> dict:
        return {
            "name": "Jane Doe",
            "skills": ["Python", "FastAPI", "AWS"],
            "experience": [{"title": "Backend Developer", "duration": "3 years"}]
        }

    parse = parse_resume


class FakeEvaluator:
    def evaluate(self, candidate_profile: dict, job_description: str) -> dict:
        return {
            "score": 90,
            "fit": "High",
            "reasoning": "Strong match with Python and AWS experience."
        }


class FakeSearchEngine:
    def __init__(self, knowledge_base=None):
        self.knowledge_base = knowledge_base

    def search(self, query: str) -> List[dict]:
        return [
            {
                "candidate_id": "candidate_001",
                "matches": True,
                "evidence": ["3 years experience with Python"]
            }
        ]


class FakeCopilot:
    def ask(self, question: str, candidates: List[Any]) -> str:
        return f"John Doe is a good match for: {question}"


# --- TEST CASES ---

def test_v2_pipeline_initialization():
    pipeline = V2RecruitingPipeline(
        parser=FakeParser(),
        evaluator=FakeEvaluator(),
        search_engine=FakeSearchEngine(),
        copilot=FakeCopilot()
    )

    assert pipeline.parser is not None
    assert pipeline.evaluator is not None
    assert pipeline.knowledge_base is not None
    assert pipeline.search_engine is not None
    assert pipeline.copilot is not None


def test_v2_pipeline_add_and_get_candidates():
    pipeline = V2RecruitingPipeline(
        parser=FakeParser(),
        evaluator=FakeEvaluator(),
        search_engine=FakeSearchEngine(),
        copilot=FakeCopilot()
    )

    profile = pipeline.add_resume("candidate_001", "dummy/path/resume.pdf")
    candidates = pipeline.get_candidates()

    assert profile["name"] == "Jane Doe"
    assert len(candidates) == 1


def test_v2_pipeline_evaluate_candidate():
    pipeline = V2RecruitingPipeline(
        parser=FakeParser(),
        evaluator=FakeEvaluator(),
        search_engine=FakeSearchEngine(),
        copilot=FakeCopilot()
    )

    pipeline.add_resume("candidate_001", "dummy/path/resume.pdf")
    result = pipeline.evaluate_candidate("candidate_001", "Looking for a Python developer")

    assert result["score"] == 90
    assert result["fit"] == "High"


def test_v2_pipeline_evaluate_missing_candidate():
    pipeline = V2RecruitingPipeline(
        parser=FakeParser(),
        evaluator=FakeEvaluator(),
        search_engine=FakeSearchEngine(),
        copilot=FakeCopilot()
    )

    with pytest.raises(ValueError, match="Candidate 'unknown_id' not found."):
        pipeline.evaluate_candidate("unknown_id", "Python Developer")


def test_v2_pipeline_search():
    pipeline = V2RecruitingPipeline(
        parser=FakeParser(),
        evaluator=FakeEvaluator(),
        search_engine=FakeSearchEngine(),
        copilot=FakeCopilot()
    )

    results = pipeline.search_candidates("Find backend developers with Python")

    assert len(results) == 1
    assert results[0]["candidate_id"] == "candidate_001"


def test_v2_copilot():
    pipeline = V2RecruitingPipeline(
        parser=FakeParser(),
        evaluator=FakeEvaluator(),
        search_engine=FakeSearchEngine(),
        copilot=FakeCopilot()
    )

    response = pipeline.ask_copilot("Who matches this backend role?")

    assert "John Doe" in response