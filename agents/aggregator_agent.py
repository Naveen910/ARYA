from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from ARYA.config import GOOGLE_API_KEY

aggregator_agent = Agent(
    name="AggregatorAgent",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),
    instruction="""
Merge all signals:
- news_output
- sentiment_output
- technical_output
- macro_output

Return final ETF signal:
{
  "final_signal": "BUY / SELL / HOLD",
  "confidence": 0-100,
  "rationale": ""
}
""",
    output_key="final_output"
)
