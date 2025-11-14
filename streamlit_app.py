"""Streamlit front-end for building an EVP."""
from __future__ import annotations

import streamlit as st

from evp_tool.config import OpenAISettings
from evp_tool.workflow import EVPWorkflow


def _render_sources(documents):
    for doc in documents:
        with st.expander(f"{doc.source_type}: {doc.url}"):
            st.write(doc.content)


def main() -> None:
    st.set_page_config(page_title="EVP Builder", layout="wide")
    st.title("Employee Value Proposition Builder")
    st.caption(
        "Enter the company name and website. The app will collect information from "
        "press releases, Glassdoor, and company reports before drafting the EVP."
    )

    with st.sidebar:
        st.header("OpenAI settings")
        st.write("Values default to environment variables if left blank.")
        api_key = st.text_input("API key", type="password")
        base_url = st.text_input("Base URL", placeholder="https://api.openai.com/v1")
        model = st.text_input("Model", value="gpt-4o-mini")

    company = st.text_input("Company name", placeholder="Example: Contoso Energy")
    website = st.text_input("Official website", placeholder="https://www.contoso.com")

    run_button = st.button("Generate EVP", type="primary")

    if run_button:
        if not company or not website:
            st.error("Please provide both company name and website URL.")
            st.stop()
        try:
            settings = OpenAISettings(
                api_key=api_key or OpenAISettings.from_env().api_key,
                base_url=base_url or None,
                model=model or "gpt-4o-mini",
            )
        except RuntimeError as exc:
            st.error(str(exc))
            st.stop()

        with st.spinner("Collecting sources and synthesizing the EVP..."):
            workflow = EVPWorkflow(settings=settings)
            result = workflow.run(company=company, company_url=website)

        st.success("EVP ready!")
        st.subheader("EVP Summary")
        st.markdown(result["evp"])

        st.subheader("Sources")
        if not result["documents"]:
            st.info("No supporting documents were captured. Please verify the inputs.")
        else:
            _render_sources(result["documents"])


if __name__ == "__main__":
    main()
