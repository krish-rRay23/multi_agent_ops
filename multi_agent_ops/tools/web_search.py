from crewai.tools import tool
import requests
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@tool
def google_search(query) -> str:
    """
    Useful for researching programming methods, libraries, and examples using Google Search.
    
    Args:
        query: The search query string
        
    Returns:
        str: Search results with titles and links
    """
    if not SERPER_API_KEY:
        return "Google search unavailable - SERPER_API_KEY not configured"
    
    try:
        # Handle different input formats that CrewAI might send
        if isinstance(query, dict):
            # Extract the actual query from dict format
            if 'description' in query:
                search_query = str(query['description'])
            elif 'query' in query:
                search_query = str(query['query'])
            elif 'q' in query:
                search_query = str(query['q'])
            else:
                # If it's a dict with unknown structure, convert to string
                search_query = str(query.get(list(query.keys())[0], query))
        else:
            search_query = str(query)
        
        # Clean up the query - remove extra quotes and formatting
        search_query = search_query.strip('"\'').replace('\\"', '')
        
        if not search_query or search_query == "str":
            return "Invalid search query provided"
        
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        data = {"q": search_query}

        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            return f"Search failed with status code: {response.status_code}"
            
        results = response.json().get("organic", [])

        if not results:
            return "No search results found."

        return "\n".join([f"{r.get('title', 'No title')}: {r.get('link', 'No link')}" for r in results[:3]])
    
    except Exception as e:
        return f"Search error: {str(e)}"

# Register the function as a tool
web_search_tool = google_search
