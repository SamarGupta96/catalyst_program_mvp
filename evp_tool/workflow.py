"""High-level orchestration for building the EVP."""
from __future__ import annotations

from typing import Dict, List

from .evp_generator import generate_evp
from .config import OpenAISettings
from .sources import SourceDocument, SourceFetcher, compile_context


class EVPWorkflow:
    """Collects sources and calls the LLM."""

    def __init__(self, settings: OpenAISettings | None = None) -> None:
        self.settings = settings or OpenAISettings.from_env()
        self.fetcher = SourceFetcher()

    def run(self, *, company: str, company_url: str) -> Dict[str, List[SourceDocument] | str]:
        documents: List[SourceDocument] = []

        company_doc = self.fetcher.fetch_company_site(company_url)
        if company_doc:
            documents.append(company_doc)

        documents.extend(self.fetcher.search_press_releases(company))
        documents.extend(self.fetcher.search_glassdoor(company))
        documents.extend(self.fetcher.search_reports(company))

        context = compile_context(documents)
        evp_output = generate_evp(company, context, self.settings)
        return {
            "documents": documents,
            "evp": evp_output,
            "context": context,
        }
