from crewai.tools import tool
import requests
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@tool
def google_search(query: str) -> str:
    """
    Useful for researching programming methods, libraries, and examples using Google Search.
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query}

    response = requests.post(url, json=data, headers=headers)
    results = response.json().get("organic", [])

    if not results:
        return "No search results found."

    return "\n".join([f"{r['title']}: {r['link']}" for r in results[:3]])

# Register the function as a tool
web_search_tool = google_search
