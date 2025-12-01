from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool

from ARYA.config import GOOGLE_API_KEY
from ARYA.tools.ohlcv_tool import fetch_ohlcv

technical_agent = Agent(
    name="TechnicalAgent",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),
    instruction="""
    You are the Technical Analysis Agent.
    
    Always call the fetch_ohlcv tool to retrieve OHLCV.
    Then compute technical indicators:
    - SMA / EMA moving averages
    - RSI
    - MACD
    - Volatility
    - Trend direction

    Return JSON:
    {
        "symbol": "...",
        "indicators": {...},
        "trend": "...",
        "sentiment": "bullish | bearish | neutral"
    }
    """,
    tools=[fetch_ohlcv],
    output_key="technical_output"
)
