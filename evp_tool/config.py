"""Configuration helpers for the EVP streamlit app."""
from __future__ import annotations

import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class OpenAISettings:
    """Holds OpenAI connection metadata."""

    api_key: str
    base_url: str | None = None
    model: str = "gpt-4o-mini"

    @classmethod
    def from_env(cls) -> "OpenAISettings":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing OPENAI_API_KEY environment variable. Set it before running the app."
            )
        base_url = os.getenv("OPENAI_BASE_URL")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return cls(api_key=api_key, base_url=base_url, model=model)

    def build_client(self) -> OpenAI:
        """Create an OpenAI client with the stored credentials."""

        return OpenAI(api_key=self.api_key, base_url=self.base_url)

    def validate(self) -> None:
        """Ensures the credentials can reach the OpenAI API before running the workflow."""

        client = self.build_client()
        try:
            # Listing models is a lightweight way to ensure the key/base URL combo works.
            client.models.list()
        except Exception as exc:  # pragma: no cover - requires network access
            raise RuntimeError(
                "Unable to validate the OpenAI credentials. Double-check the API key, "
                "base URL, and that the selected model is accessible."
            ) from exc


MAX_CHARS_PER_SOURCE = 4000
"""We limit the amount of text per source so prompts stay within model context."""
