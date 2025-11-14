"""Source gathering utilities for EVP generation."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from .config import MAX_CHARS_PER_SOURCE


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/15.1 Safari/605.1.15"
)


@dataclass
class SourceDocument:
    """Structured view of a fetched document."""

    title: str
    url: str
    source_type: str
    content: str


class SourceFetcher:
    """Loads data from required external sources."""

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})

    def fetch_company_site(self, url: str) -> SourceDocument | None:
        return self._fetch_url(url, "Company website")

    def search_press_releases(self, company: str, limit: int = 3) -> List[SourceDocument]:
        return self._search_and_fetch(
            query=f"{company} press release", source_type="Press release", limit=limit
        )

    def search_glassdoor(self, company: str, limit: int = 2) -> List[SourceDocument]:
        return self._search_and_fetch(
            query=f"{company} Glassdoor employee reviews", source_type="Glassdoor", limit=limit
        )

    def search_reports(self, company: str, limit: int = 2) -> List[SourceDocument]:
        return self._search_and_fetch(
            query=f"{company} annual report site:investor", source_type="Company report", limit=limit
        )

    def _search_and_fetch(
        self, *, query: str, source_type: str, limit: int
    ) -> List[SourceDocument]:
        documents: List[SourceDocument] = []
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=limit):
                url = result.get("href") or result.get("url")
                if not url or "wikipedia.org" in url:
                    continue
                doc = self._fetch_url(url, source_type)
                if doc:
                    documents.append(doc)
        return documents

    def _fetch_url(self, url: str, source_type: str) -> SourceDocument | None:
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
        except requests.RequestException:
            return None
        text = self._clean_html(response.text)
        if not text:
            return None
        return SourceDocument(
            title=url,
            url=url,
            source_type=source_type,
            content=text[:MAX_CHARS_PER_SOURCE],
        )

    @staticmethod
    def _clean_html(raw_html: str) -> str:
        soup = BeautifulSoup(raw_html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        text = soup.get_text(separator=" ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()


def compile_context(documents: Iterable[SourceDocument]) -> str:
    """Combine fetched documents into a single prompt string."""

    sections = []
    for doc in documents:
        sections.append(
            f"Source: {doc.source_type}\nURL: {doc.url}\nContent: {doc.content}\n"
        )
    return "\n---\n".join(sections)
