#!/usr/bin/env python3
"""
Test script for the web search tool
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def direct_google_search(query):
    """Direct implementation of google search without @tool decorator"""
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    
    if not SERPER_API_KEY:
        return "Google search unavailable - SERPER_API_KEY not configured"
    
    try:
        # Handle different input formats
        if isinstance(query, dict):
            # Extract the actual query from dict format
            if 'description' in query:
                search_query = query['description']
            elif 'query' in query:
                search_query = query['query']
            else:
                search_query = str(query)
        else:
            search_query = str(query)
        
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

def test_web_search():
    """Test the web search tool functionality"""
    print("🔍 Testing Web Search Tool")
    print("=" * 40)
    
    # Check if API key is configured
    serper_key = os.getenv("SERPER_API_KEY")
    if serper_key:
        print(f"✅ SERPER_API_KEY found: {serper_key[:10]}...")
    else:
        print("❌ SERPER_API_KEY not found")
        return False
    
    # Test 1: Simple string query
    print("\n🧪 Test 1: Simple string query")
    test_query = "Python programming tutorial"
    print(f"Query: {test_query}")
    
    try:
        result = direct_google_search(test_query)
        print("Result:")
        print("-" * 20)
        print(result)
        print("-" * 20)
        
        if "Search error:" in result:
            print("❌ Test 1 failed with error")
            return False
        elif "Google search unavailable" in result:
            print("❌ Test 1 failed - API key issue")
            return False
        elif "No search results found" in result:
            print("⚠️ Test 1 - No results but no error")
        else:
            print("✅ Test 1 passed")
            
    except Exception as e:
        print(f"❌ Test 1 failed with exception: {e}")
        return False
    
    # Test 2: Dict input (to test the handling we added)
    print("\n🧪 Test 2: Dictionary input")
    test_dict = {"description": "Discord bot tutorial", "type": "str"}
    print(f"Query: {test_dict}")
    
    try:
        result = direct_google_search(test_dict)
        print("Result:")
        print("-" * 20)
        print(result)
        print("-" * 20)
        
        if "Search error:" in result:
            print("❌ Test 2 failed with error")
        else:
            print("✅ Test 2 passed - handled dict input")
            
    except Exception as e:
        print(f"❌ Test 2 failed with exception: {e}")
    
    print("\n🎯 Web search tool test completed!")
    return True

if __name__ == "__main__":
    test_web_search()
