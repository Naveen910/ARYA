from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.models.google_llm import Gemini

from ARYA.agents.news_agent import news_agent
from ARYA.agents.sentiment_agent import sentiment_agent
from ARYA.agents.technical_agent import technical_agent
from ARYA.agents.macro_agent import macro_agent
from ARYA.agents.aggregator_agent import aggregator_agent
from ARYA.config import GOOGLE_API_KEY

coordinator_agent = Agent(
    name="ETFCoordinator",
    model=Gemini(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY),
    instruction="""
You are the ETF signal coordinator.
Steps:
1. Call NewsAgent → get market & company news
2. Call SentimentAgent → generate sentiment score
3. Call TechnicalAgent → extract technical indicators
4. Call MacroAgent → understand macro regime
5. Call AggregatorAgent → merge all and output final BUY/SELL/HOLD signal
""",
    tools=[
        AgentTool(news_agent),
        AgentTool(sentiment_agent),
        AgentTool(technical_agent),
        AgentTool(macro_agent),
        AgentTool(aggregator_agent)
    ],
    output_key="etf_signal"
)
