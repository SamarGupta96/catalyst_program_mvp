# EVP Builder

A lightweight Streamlit application that researches publicly available sources and
uses OpenAI to generate an Employee Value Proposition (EVP) structured around the
four McKinsey quadrants: Great Company, Great People, Great Rewards, and Great Job.

## Features
- Pulls data from the company website, press releases, Glassdoor references, and
  company reports using DuckDuckGo search.
- Cleans raw HTML into concise snippets ready for prompting.
- Uses OpenAI's Chat Completions API to synthesize an EVP aligned with the guiding
  questions from the provided PowerPoint.
- Displays the generated EVP along with all collected source excerpts.

## Getting started
1. Create a Python environment and install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the required environment variables with your enterprise OpenAI details:
   ```bash
   export OPENAI_API_KEY="sk-..."
   export OPENAI_BASE_URL="https://your-enterprise-endpoint/v1"  # optional
   export OPENAI_MODEL="gpt-4o-mini"  # optional override
   ```
3. Launch the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
4. Provide the company name and official website URL. Optionally override the
   OpenAI credentials from the sidebar. Click **Generate EVP** to trigger the
   workflow.

## Notes
- The DuckDuckGo-based search intentionally skips Wikipedia and blog domains to
  respect the source restrictions.
- Some sources (e.g., Glassdoor) may block automated access. In such cases, the
  app will proceed with the sources it can successfully fetch and highlight gaps
  in the final EVP.
