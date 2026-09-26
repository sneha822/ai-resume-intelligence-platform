from src.ai.copilot import RecruiterCopilot


class FakeLLMClient:

    def generate(self, prompt, system_prompt=None):

        return (
            "John Doe has strong Python and AWS "
            "experience based on his candidate profile."
        )


def sample_candidates():

    return [
        {
            "candidate_id": "candidate_001",
            "profile": {
                "name": "John Doe",
                "skills": [
                    "Python",
                    "AWS",
                    "FastAPI"
                ],
                "experience": [
                    {
                        "company": "ABC Technologies",
                        "role": "Backend Developer",
                        "duration": "3 years"
                    }
                ]
            }
        }
    ]


def test_copilot_builds_context():

    copilot = RecruiterCopilot(
        llm_client=FakeLLMClient()
    )

    context = copilot.build_context(
        sample_candidates()
    )

    assert "John Doe" in context
    assert "Python" in context
    assert "AWS" in context


def test_copilot_answers_question():

    copilot = RecruiterCopilot(
        llm_client=FakeLLMClient()
    )

    answer = copilot.ask(
        "Who has Python and AWS experience?",
        sample_candidates()
    )

    assert "John Doe" in answer
    assert "Python" in answer
    assert "AWS" in answer


def test_conversation_history():

    copilot = RecruiterCopilot(
        llm_client=FakeLLMClient()
    )

    copilot.ask(
        "Tell me about John.",
        sample_candidates()
    )

    assert len(
        copilot.conversation_history
    ) == 2


def test_clear_history():

    copilot = RecruiterCopilot(
        llm_client=FakeLLMClient()
    )

    copilot.ask(
        "Tell me about John.",
        sample_candidates()
    )

    copilot.clear_history()

    assert copilot.conversation_history == []