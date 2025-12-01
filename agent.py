from ARYA.agents.coordinator_agent import coordinator_agent
from google.adk.runners import InMemoryRunner

root_agent = coordinator_agent

runner = InMemoryRunner(agent=root_agent)