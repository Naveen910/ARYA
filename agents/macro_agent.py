from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from ARYA.config import GOOGLE_API_KEY

macro_agent = Agent(
    name="MacroAgent",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),
    instruction="""
Analyze macroeconomic regime using:
- global markets
- interest rates
- inflation trends
- risk sentiment

Return:
{
  "macro_summary": "",
  "macro_sentiment": "Bullish/Bearish/Neutral"
}
""",
    output_key="macro_output"
)
