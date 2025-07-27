#!/usr/bin/env python3
"""
Multi-Agent Development System - Ultra Simple Version
The simplest possible working version
"""

from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv

load_dotenv()

# Configure LLM directly
llm = LLM(
    model=os.getenv("OPENAI_MODEL", "llama3-8b-8192"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

print("🚀 Ultra Simple Multi-Agent System")
print("=" * 35)

# Get user input
project = input("What to build? ").strip() or "todo app"
print(f"📋 Building: {project}")

# Create a single simple agent
agent = Agent(
    role='Developer',
    goal='Provide helpful development guidance',
    backstory='You are a helpful developer who gives practical advice.',
    llm=llm,
    verbose=True
)

# Create a simple task
task = Task(
    description=f"Give 3 simple steps to build a {project}. Be very brief.",
    agent=agent,
    expected_output="3 clear development steps"
)

# Create crew
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=False
)

print("🔄 Processing...")

try:
    result = crew.kickoff()
    print("\n✅ Result:")
    print("-" * 20)
    print(result)
    print("-" * 20)
    print("✅ Success!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    if "rate_limit" in str(e).lower():
        print("💡 Rate limit - wait 1 minute and try again")
