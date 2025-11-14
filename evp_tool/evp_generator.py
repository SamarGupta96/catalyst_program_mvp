"""Prompting utilities to convert raw context into an EVP."""
from __future__ import annotations

from textwrap import dedent

from .config import OpenAISettings


EVP_DIMENSIONS = {
    "Great Company": [
        "How well is the business managed?",
        "Is there a well-defined culture and are values appealing to employees?",
        "What contribution does the business have on society?",
    ],
    "Great People": [
        "How does leadership motivate and inspire employees?",
        "Is top-tier management well aligned and trustworthy?",
        "How is my interaction with colleagues?",
    ],
    "Great Rewards": [
        "How are employees recognized and rewarded for performance?",
        "How does the business differentiate rewards for high performers?",
        "What are the non-monetary benefits?",
    ],
    "Great Job": [
        "Are opportunities to advance clearly defined?",
        "Are employees given opportunities to improve their skill set?",
        "How interesting and challenging is the work?",
        "What coaching and mentoring platforms exist?",
    ],
}


def format_dimension_prompt() -> str:
    """Helper that encodes the EVP guidance for the LLM."""

    lines = ["Structure your analysis using the following dimensions:"]
    for dimension, questions in EVP_DIMENSIONS.items():
        lines.append(f"- {dimension}:")
        for question in questions:
            lines.append(f"  * {question}")
    return "\n".join(lines)


def generate_evp(company: str, context: str, settings: OpenAISettings) -> str:
    """Calls the OpenAI API to summarize content into the EVP grid."""

    client = settings.build_client()
    prompt = dedent(
        f"""
        You are a communications strategist. Use the provided research snippets to craft an
        Employee Value Proposition (EVP) for {company}. Only reference the given context –
        do not invent information or rely on prohibited sources such as Wikipedia or blogs.

        {format_dimension_prompt()}

        Requirements:
        - Synthesize evidence from company website, press releases, Glassdoor, and reports.
        - Highlight proof points, differentiators, and any notable gaps per dimension.
        - Keep each answer concise (2-3 sentences per bullet) but specific.
        - Provide recommendations or open questions if information is missing.
        - Present the final answer as markdown with a level-3 heading per dimension followed
          by bullet points answering the guiding questions.

        Context:
        {context}
        """
    ).strip()

    response = client.chat.completions.create(
        model=settings.model,
        messages=[
            {"role": "system", "content": "You analyze company materials to craft EVPs."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
