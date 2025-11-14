"""Configuration helpers for the EVP streamlit app."""
from __future__ import annotations

import os
from dataclasses import dataclass


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


MAX_CHARS_PER_SOURCE = 4000
"""We limit the amount of text per source so prompts stay within model context."""
