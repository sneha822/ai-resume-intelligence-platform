from src.ai.hybrid_parser import HybridResumeParser
from src.ai.candidate_evaluator import CandidateEvaluator
from src.ai.candidate_knowledge import CandidateKnowledgeBase
from src.ai.candidate_search import NaturalLanguageCandidateSearch
from src.ai.copilot import RecruiterCopilot


class V2RecruitingPipeline:
    """
    End-to-end V2 AI recruiting pipeline.

    Responsibilities:
    - Parse resumes
    - Store structured candidate profiles
    - Evaluate candidates against a job description
    - Search candidates using natural language
    - Provide recruiter copilot functionality
    """

    def __init__(
        self,
        parser=None,
        evaluator=None,
        knowledge_base=None,
        search_engine=None,
        copilot=None,
    ):
        self.parser = parser or HybridResumeParser()
        self.evaluator = evaluator or CandidateEvaluator()

        self.knowledge_base = (
            knowledge_base or CandidateKnowledgeBase()
        )

        self.search_engine = search_engine or NaturalLanguageCandidateSearch(
            self.knowledge_base
        )

        self.copilot = copilot or RecruiterCopilot()

    def add_resume(self, candidate_id, file_path):
        """
        Parse a resume and add the candidate to the knowledge base.
        """

        if not candidate_id:
            raise ValueError("candidate_id cannot be empty.")

        if not file_path:
            raise ValueError("file_path cannot be empty.")

        profile = self.parser.parse_resume(file_path)

        self.knowledge_base.add_candidate(
            candidate_id,
            profile,
        )

        return profile

    def evaluate_candidate(
        self,
        candidate_id,
        job_description,
    ):
        """
        Evaluate one candidate against a job description.
        """

        candidate = self.knowledge_base.get_candidate(
            candidate_id
        )

        if candidate is None:
            raise ValueError(
                f"Candidate '{candidate_id}' not found."
            )

        profile = candidate.profile if hasattr(candidate, "profile") else candidate["profile"]

        return self.evaluator.evaluate(
            profile,
            job_description,
        )

    def search_candidates(self, question):
        """
        Search candidates using a natural-language recruiter query.
        """

        return self.search_engine.search(question)

    def ask_copilot(self, question, candidates=None):
        """
        Ask the recruiter copilot a question using candidate context.
        """

        if candidates is None:
            candidates = self.knowledge_base.all_candidates()

        return self.copilot.ask(
            question,
            candidates,
        )

    def get_candidates(self):
        """Return all candidates currently in the knowledge base."""

        return self.knowledge_base.all_candidates()