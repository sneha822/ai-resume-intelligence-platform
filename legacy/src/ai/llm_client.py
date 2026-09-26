import os
from typing import Optional


class LLMClient:
    """
    Provider-independent LLM client interface.

    The rest of the application should communicate
    with the LLM through this class rather than
    directly calling a provider.
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.provider = (
            provider
            or os.getenv(
                "LLM_PROVIDER",
                "ollama"
            )
        )

        self.model = (
            model
            or os.getenv(
                "LLM_MODEL",
                "llama3.2"
            )
        )

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate a response from the configured LLM.

        Provider-specific implementation will be
        connected here without changing callers.
        """

        if not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        if self.provider == "ollama":
            return self._generate_ollama(
                prompt,
                system_prompt
            )

        if self.provider == "openai":
            return self._generate_openai(
                prompt,
                system_prompt
            )

        raise ValueError(
            f"Unsupported LLM provider: "
            f"{self.provider}"
        )

    def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str]
    ) -> str:
        """
        Ollama implementation.

        Actual API integration will be completed
        during the V2 integration stages.
        """

        try:
            import ollama
        except ImportError as error:
            raise ImportError(
                "Ollama support requires the "
                "'ollama' package."
            ) from error

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        return response["message"]["content"]

    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str]
    ) -> str:
        """
        OpenAI implementation.

        Kept separate so the rest of the application
        does not depend on provider-specific code.
        """

        try:
            from openai import OpenAI
        except ImportError as error:
            raise ImportError(
                "OpenAI support requires the "
                "'openai' package."
            ) from error

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        client = OpenAI(
            api_key=api_key
        )

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0
        )

        return response.choices[0].message.content