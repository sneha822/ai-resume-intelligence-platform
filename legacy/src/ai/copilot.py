from src.ai.llm_client import LLMClient
from src.ai.prompts import COPILOT_SYSTEM_PROMPT


class RecruiterCopilot:
    """
    AI assistant for recruiter-facing candidate questions.

    The Copilot receives candidate context and uses the LLM
    to generate grounded responses with conversation history.
    """

    def __init__(self, llm_client=None):
        self.llm_client = llm_client or LLMClient()
        self.conversation_history = []

    @property
    def history(self):
        """Property alias for backward compatibility with self.history."""
        return self.conversation_history

    @history.setter
    def history(self, value):
        self.conversation_history = value

    def build_context(self, candidates):
        """
        Convert candidate records into context for the LLM.
        """
        if not candidates:
            return "No candidate information is available."

        context_parts = []
        for candidate in candidates:
            candidate_id = candidate.get("candidate_id", "unknown")
            profile = candidate.get("profile", {})
            context_parts.append(
                f"""
CANDIDATE ID: {candidate_id}

PROFILE:
{profile}
"""
            )

        return "\n".join(context_parts)

    def _format_history(self) -> str:
        """
        Format previous conversation turns into a string for prompt context.
        """
        if not self.conversation_history:
            return "No prior conversation history."

        turns = []
        for turn in self.conversation_history:
            role = turn.get("role", "user")
            content = turn.get("content", turn.get("question", turn.get("answer", "")))
            turns.append(f"{role.capitalize()}: {content}")

        return "\n".join(turns)

    def build_prompt(self, question, candidates):
        context = self.build_context(candidates)
        history_str = self._format_history()

        return f"""
CANDIDATE CONTEXT:

{context}

CONVERSATION HISTORY:

{history_str}

RECRUITER QUESTION:

{question}

Answer the recruiter's question using only the candidate context provided above.
Consider the conversation history if the question is a follow-up.
"""

    def ask(self, question, candidates):
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        prompt = self.build_prompt(question, candidates)

        response = self.llm_client.generate(
            prompt,
            system_prompt=COPILOT_SYSTEM_PROMPT
        )

        # Append separate history entries for user query and AI response
        self.conversation_history.append({"role": "user", "content": question})
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def clear_history(self):
        """
        Reset conversation memory.
        """
        self.conversation_history = []