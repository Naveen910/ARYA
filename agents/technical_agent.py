from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from ARYA.config import GOOGLE_API_KEY

technical_agent = Agent(
    name="TechnicalAgent",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),
    instruction="""
You compute technical indicators using the ohlcv data:
- Moving averages
- RSI
- MACD
- Trend direction
Return JSON of indicators and technical sentiment.
""",
    output_key="technical_output"
)
