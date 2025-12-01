from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from ARYA.config import GOOGLE_API_KEY

sentiment_agent = Agent(
    name="SentimentAgent",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),
    instruction="""
You analyze news_output and compute overall sentiment.
Return:
{
  "sentiment_score": float(-1 to +1),
  "label": "Bullish / Bearish / Neutral"
}
""",
    output_key="sentiment_output"
)
