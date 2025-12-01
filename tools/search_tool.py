import os
from google.adk.tools.google_search import GoogleSearchTool
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
search_tool = GoogleSearchTool(api_key=GOOGLE_API_KEY)

def fetch_news(query: str, num_results=5):
    results = search_tool.run({"query": query, "num_results": num_results})
    # Extract useful info
    news_list = []
    for r in results.get("results", []):
        news_list.append({"title": r.get("title"), "link": r.get("link"), "snippet": r.get("snippet")})
    return news_list
