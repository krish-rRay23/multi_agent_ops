from crewai.tools import tool
import requests
import os

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@tool
def google_search(query) -> str:
    """
    Research tool that either uses web search or provides knowledge-based recommendations.
    
    Args:
        query: The search query string
        
    Returns:
        str: Research findings or recommendations
    """
    
    # Handle different input formats from CrewAI
    if isinstance(query, dict):
        if 'description' in query:
            search_query = str(query['description'])
        elif 'query' in query:
            search_query = str(query['query'])
        else:
            search_query = str(query.get(list(query.keys())[0], query))
    else:
        search_query = str(query)
    
    search_query = search_query.strip('"\'').replace('\\"', '').lower()
    
    # If no API key, provide knowledge-based recommendations
    if not SERPER_API_KEY:
        return provide_knowledge_based_research(search_query)
    
    # Try web search if API key available
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        data = {"q": search_query}

        response = requests.post(url, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            results = response.json().get("organic", [])
            if results:
                return "\n".join([f"{r.get('title', 'No title')}: {r.get('link', 'No link')}" for r in results[:3]])
        
        # Fallback to knowledge-based if web search fails
        return provide_knowledge_based_research(search_query)
        
    except Exception as e:
        return provide_knowledge_based_research(search_query)

def provide_knowledge_based_research(query):
    """Provide knowledge-based research recommendations"""
    
    # Common programming tools and libraries by category
    recommendations = {
        "cli": [
            "argparse - Command line argument parsing",
            "click - Creating beautiful command line interfaces", 
            "typer - Type hints for CLI applications"
        ],
        "todo": [
            "sqlite3 - Built-in database for persistence",
            "json - Simple file-based storage",
            "datetime - For timestamps and due dates"
        ],
        "web": [
            "requests - HTTP library for web scraping",
            "beautifulsoup4 - HTML/XML parsing",
            "selenium - Browser automation"
        ],
        "api": [
            "fastapi - Modern web framework for APIs",
            "flask - Lightweight web framework",
            "uvicorn - ASGI server for FastAPI"
        ],
        "data": [
            "pandas - Data manipulation and analysis",
            "numpy - Numerical computing",
            "matplotlib - Data visualization"
        ],
        "bot": [
            "discord.py - Discord bot development",
            "python-telegram-bot - Telegram bot API",
            "asyncio - Asynchronous programming"
        ],
        "file": [
            "pathlib - Modern path handling",
            "shutil - File operations",
            "os - Operating system interface"
        ],
        "calculator": [
            "math - Mathematical functions",
            "decimal - Precise decimal arithmetic",
            "operator - Standard operators as functions"
        ]
    }
    
    # Find relevant recommendations
    results = []
    for category, libs in recommendations.items():
        if category in query:
            results.extend(libs)
    
    # If no specific match, provide general recommendations
    if not results:
        if any(word in query for word in ['python', 'script', 'app', 'tool']):
            results = [
                "Standard Library - Use built-in Python modules first",
                "pip - Package installer for additional libraries",
                "pathlib - Modern file path handling"
            ]
        else:
            results = [
                "Research Query: " + query,
                "Recommendation: Use Python standard library when possible",
                "Consider: Popular libraries like requests, pandas, or click"
            ]
    
    return "Knowledge-based recommendations:\n" + "\n".join(f"• {rec}" for rec in results[:3])

# Register the function as a tool
web_search_tool = google_search
