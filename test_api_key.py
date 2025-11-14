"""Utility script to verify OpenAI API credentials."""
from __future__ import annotations

import argparse
import os
import sys

from evp_tool.config import OpenAISettings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Checks whether the supplied OpenAI API key/base URL combination can "
            "successfully connect to the service."
        )
    )
    parser.add_argument(
        "--api-key",
        help=(
            "OpenAI API key to validate. Defaults to the OPENAI_API_KEY environment variable."
        ),
    )
    parser.add_argument(
        "--base-url",
        help=(
            "Optional custom base URL for the OpenAI-compatible endpoint. Defaults to "
            "OPENAI_BASE_URL if set."
        ),
    )
    parser.add_argument(
        "--model",
        default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        help=(
            "Model name to use during validation. Defaults to the OPENAI_MODEL environment "
            "variable or 'gpt-4o-mini'."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "Missing API key. Provide --api-key or set the OPENAI_API_KEY environment variable.",
            file=sys.stderr,
        )
        return 1

    base_url = args.base_url or os.getenv("OPENAI_BASE_URL")
    settings = OpenAISettings(api_key=api_key, base_url=base_url, model=args.model)
    try:
        settings.validate()
    except RuntimeError as exc:  # pragma: no cover - requires network access
        print(str(exc), file=sys.stderr)
        return 2

    print(f"OpenAI credentials validated successfully for model '{settings.model}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
