#!/usr/bin/env python3
"""
Multi-Agent Development System - No Web Search Version
A fully functional version without web search to avoid rate limiting issues
"""

from crewai import Crew, Task
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from memory.vector_store import VectorMemory
from config.llm_config import get_shared_llm
import os
import time
from dotenv import load_dotenv

load_dotenv()

def test_config():
    """Test the configuration and display debug info"""
    print("🚀 Multi-Agent Development System (No Web Search)")
    print("=" * 50)
    print(f"DEBUG: OPENAI_API_KEY = {os.getenv('OPENAI_API_KEY')[:20]}...")
    print(f"DEBUG: OPENAI_API_BASE = {os.getenv('OPENAI_API_BASE')}")
    print(f"DEBUG: OPENAI_MODEL = {os.getenv('OPENAI_MODEL')}")
    print("=" * 50)
    
    # Test vector store
    try:
        vector_memory = VectorMemory()
        print("✅ Vector store initialized successfully")
    except Exception as e:
        print(f"❌ Vector store failed: {e}")
        return False
    
    # Test LLM
    try:
        llm = get_shared_llm()
        print("✅ LLM Configuration: Successfully loaded")
    except Exception as e:
        print(f"❌ LLM Configuration failed: {e}")
        return False
    
    return True

def get_project_query():
    """Get project description from user"""
    print("🎯 What would you like to build today?")
    print("Examples:")
    print("- CLI To-Do app with database")
    print("- Simple web scraper")
    print("- Discord bot with commands")
    print("- REST API with FastAPI")
    print("- Data analysis tool")
    query = input("📝 Enter your project description: ").strip()
    return query if query else "CLI To-Do app with database"

def create_simple_researcher_agent(query="CLI To-Do app"):
    """Create a researcher agent that doesn't use web search"""
    from crewai import Agent
    
    try:
        vector_memory = VectorMemory()
        related_plans = vector_memory.search(query, k=3)
        context = "\\n".join([doc.page_content for doc in related_plans]) if related_plans else "No related plans found."
        print(f"🔍 Found {len(related_plans)} related memories")
    except Exception as e:
        print(f"⚠️ Vector memory error: {e}")
        context = "No related plans found."
    
    return Agent(
        role='Technical Researcher',
        goal='Provide detailed technical recommendations based on knowledge and experience',
        backstory=(
            "You're a technical researcher with deep knowledge of programming tools, libraries, and best practices. "
            "You provide comprehensive research and recommendations based on your extensive experience. "
            "You focus on popular, well-documented solutions and proven patterns.\\n\\n"
            f"Here's relevant memory from past plans:\\n{context}"
        ),
        llm=get_shared_llm(),
        allow_delegation=False,
        verbose=True
    )

def create_noweb_crew(query):
    """Create a crew without web search functionality"""
    print(f"🔧 Creating development team for: {query}")
    
    # Initialize vector memory
    try:
        vector_memory = VectorMemory()
        print("✅ Vector store initialized successfully")
    except Exception as e:
        print(f"⚠️ Vector store initialization warning: {e}")
    
    # Create agents
    planner = PlannerAgent().build()
    researcher = create_simple_researcher_agent(query)  # No web search
    coder = CoderAgent().build()
    reviewer = ReviewerAgent().build()
    
    # Create tasks
    planning_task = Task(
        description=f"Create a development plan for: {query}. Include key steps and dependencies.",
        agent=planner,
        expected_output="A detailed development plan with clear steps and dependencies"
    )
    
    research_task = Task(
        description=f"Research tools and libraries for: {query}. Provide recommendations based on your knowledge.",
        agent=researcher,
        expected_output="Technical recommendations with libraries, tools, and best practices"
    )
    
    coding_task = Task(
        description=f"Write the main application code for: {query}. Use the research findings.",
        agent=coder,
        expected_output="Complete, functional Python code with proper documentation"
    )
    
    review_task = Task(
        description="Review the code and provide feedback for improvements.",
        agent=reviewer,
        expected_output="Code review with suggestions for improvements and best practices"
    )
    
    # Create crew
    crew = Crew(
        agents=[planner, researcher, coder, reviewer],
        tasks=[planning_task, research_task, coding_task, review_task],
        verbose=True,
        memory=False  # Disable crew memory to reduce token usage
    )
    
    return crew

def main():
    """Main function to run the development process"""
    # Test configuration
    if not test_config():
        print("❌ Configuration test failed. Exiting.")
        return
    
    # Get project query
    query = get_project_query()
    
    # Create and run crew
    crew = create_noweb_crew(query)
    
    print("🚀 Starting multi-agent development process...")
    print(f"📋 Project: {query}")
    print("👥 Team: Planner → Researcher → Coder → Reviewer")
    print("🧠 Memory: Vector storage enabled")
    print("🔍 Web Search: Disabled (Knowledge-based)")
    print("📁 File Operations: Enabled")
    print("⚡ Mode: Simplified")
    print("-" * 60)
    
    try:
        start_time = time.time()
        result = crew.kickoff()
        end_time = time.time()
        
        print("=" * 60)
        print("🎉 Development process completed successfully!")
        print(f"⏱️ Total time: {end_time - start_time:.1f} seconds")
        print("=" * 60)
        print("📋 Final Output:")
        print(result)
        
        # Save to vector memory for future reference
        try:
            vector_memory = VectorMemory()
            vector_memory.add_document(f"Project: {query}", str(result))
            print("💾 Results saved to vector memory for future reference")
        except Exception as e:
            print(f"⚠️ Could not save to vector memory: {e}")
            
    except Exception as e:
        print(f"❌ Development process failed: {e}")
        print("💡 Try adjusting the project description or check your API configuration")

if __name__ == "__main__":
    main()
