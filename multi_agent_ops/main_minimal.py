#!/usr/bin/env python3
"""
Multi-Agent Development System - Minimal Version
Ultra-lightweight version to avoid rate limits completely
"""

from crewai import Crew, Task, Agent
from config.llm_config import get_shared_llm
import os
import time
from dotenv import load_dotenv

load_dotenv()

def test_config():
    """Test the configuration"""
    print("🚀 Minimal Multi-Agent Development System")
    print("=" * 40)
    print(f"API Key: {os.getenv('OPENAI_API_KEY')[:20]}...")
    print(f"Model: {os.getenv('OPENAI_MODEL')}")
    print("=" * 40)
    return True

def get_project_query():
    """Get project description from user"""
    print("What would you like to build?")
    query = input("Project: ").strip()
    return query if query else "simple todo app"

def create_minimal_agent(role, goal):
    """Create a minimal agent with shared LLM"""
    return Agent(
        role=role,
        goal=goal,
        backstory=f"You are an expert {role.lower()} who provides concise, practical solutions.",
        llm=get_shared_llm(),
        allow_delegation=False,
        verbose=True
    )

def run_single_task(query, task_type="plan"):
    """Run just one task to avoid rate limits"""
    print(f"🔧 Creating {task_type} for: {query}")
    
    if task_type == "plan":
        agent = create_minimal_agent("Planner", "Create a simple development plan")
        task_desc = f"Create a basic plan to build: {query}. Keep it short and practical."
        expected = "A simple development plan with 3-5 steps"
    elif task_type == "code":
        agent = create_minimal_agent("Coder", "Write basic Python code")
        task_desc = f"Write simple Python code for: {query}. Include main functionality only."
        expected = "Working Python code with basic features"
    else:
        agent = create_minimal_agent("Researcher", "Find tools and libraries")
        task_desc = f"List 2-3 key libraries needed for: {query}. Be brief."
        expected = "Short list of recommended libraries"
    
    # Create single task
    task = Task(
        description=task_desc,
        agent=agent,
        expected_output=expected
    )
    
    # Create crew with single task
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
        memory=False
    )
    
    return crew

def main():
    """Main function"""
    if not test_config():
        return
    
    query = get_project_query()
    
    print(f"📋 Project: {query}")
    print("⚡ Mode: Single task to avoid rate limits")
    print("-" * 40)
    
    # Ask user which task to run
    print("Choose task:")
    print("1. Planning")
    print("2. Research") 
    print("3. Coding")
    choice = input("Choice (1-3): ").strip()
    
    task_map = {"1": "plan", "2": "research", "3": "code"}
    task_type = task_map.get(choice, "plan")
    
    try:
        start_time = time.time()
        crew = run_single_task(query, task_type)
        result = crew.kickoff()
        end_time = time.time()
        
        print("=" * 40)
        print("✅ Task completed!")
        print(f"⏱️ Time: {end_time - start_time:.1f}s")
        print("=" * 40)
        print("📋 Output:")
        print(result)
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        if "rate_limit" in str(e).lower():
            print("💡 Rate limit hit. Try again in 1 minute.")
        else:
            print("💡 Try a simpler project description.")

if __name__ == "__main__":
    main()
