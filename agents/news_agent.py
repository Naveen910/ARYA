from google.adk.agents import Agent
from google.adk.tools import FunctionTool, google_search
from google.adk.models.google_llm import Gemini

from ARYA.tools.etf_holdings import get_etf_holdings
from ARYA.config import GOOGLE_API_KEY

news_agent = Agent(
    name="NewsAgent",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),
    instruction="""
You are the advanced ETF news intelligence agent.

Workflow:
1. Fetch ETF underlying companies using get_etf_holdings.
2. Search the internet using google_search for:
    - ETF name
    - Sector news
    - Top underlying companies
    - Macro market news
3. Summarize all news:
    - sentiment (positive/negative/neutral)
    - relevance
    - impact score (1–10)
4. Return JSON:
{
  "company_news": [],
  "sector_news": [],
  "macro_news": [],
  "merged_summary": "",
  "overall_sentiment": ""
}
""",
    tools=[
        google_search,
    ],
    output_key="news_output"
)
