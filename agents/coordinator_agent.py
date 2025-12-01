from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini

from ARYA.agents.news_agent import news_agent
from ARYA.agents.sentiment_agent import sentiment_agent
from ARYA.agents.technical_agent import technical_agent
from ARYA.agents.macro_agent import macro_agent
from ARYA.agents.aggregator_agent import aggregator_agent

from ARYA.tools.ohlcv_tool import fetch_ohlcv

from ARYA.config import GOOGLE_API_KEY


coordinator_agent = Agent(
    name="ETFCoordinator",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),

    instruction="""
    You are the ETF signal coordinator.

    Your workflow:
    1. Call fetch_ohlcv to retrieve OHLCV market data.
    2. Pass this data to NewsAgent → get market & company news.
    3. Call SentimentAgent → convert news into sentiment score.
    4. Call TechnicalAgent → compute technical indicators (MA, RSI, MACD).
    5. Call MacroAgent → determine macroeconomic environment.
    6. Call AggregatorAgent → merge all outputs into final BUY/SELL/HOLD.

    Always return a structured JSON under `etf_signal`.
    """,

    tools=[
        fetch_ohlcv,         
        AgentTool(news_agent),
        AgentTool(sentiment_agent),
        AgentTool(technical_agent),
        AgentTool(macro_agent),
        AgentTool(aggregator_agent)
    ],

    output_key="etf_signal"
)
