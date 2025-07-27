#!/usr/bin/env python3
"""
Advanced Multi-Agent Development System - Optimized for Rate Limits
Full-featured system with web search, file operations, and memory - optimized for Groq
"""

from crewai import Crew, Task
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from memory.vector_store import VectorMemory
from config.llm_config import get_shared_llm
import time
import os

from dotenv import load_dotenv
load_dotenv()

def test_config():
    """Test and display configuration"""
    print("🚀 Advanced Multi-Agent System (Rate Limit Optimized)")
    print("=" * 55)
    print(f"API Key: {os.getenv('OPENAI_API_KEY')[:20]}..." if os.getenv('OPENAI_API_KEY') else "❌ Not set")
    print(f"Model: {os.getenv('OPENAI_MODEL')}")
    print(f"Base URL: {os.getenv('OPENAI_API_BASE')}")
    print("=" * 55)
    
    try:
        vector_memory = VectorMemory()
        print("✅ Vector memory initialized")
        llm = get_shared_llm()
        print("✅ LLM configuration loaded")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def get_project_query():
    """Get project requirements from user"""
    print("\n🎯 What would you like to build?")
    print("Examples: CLI todo app, Discord bot, Web scraper, REST API")
    
    query = input("\n📝 Project: ").strip()
    return query if query else "CLI todo app with database"

def create_optimized_crew(project_query):
    """Create crew optimized for rate limits"""
    
    # Initialize agents
    print("🔧 Initializing development team...")
    planner = PlannerAgent().build()
    researcher = ResearcherAgent().build(query=project_query)
    coder = CoderAgent().build()
    reviewer = ReviewerAgent().build()
    
    print("✅ Team ready: Planner, Researcher, Coder, Reviewer")
    
    # Shorter, focused task descriptions to reduce token usage
    plan_task = Task(
        description=f"Create development plan for: {project_query}. Include steps and dependencies.",
        expected_output="Development plan with clear steps",
        agent=planner
    )

    research_task = Task(
        description=f"Research tools and libraries for: {project_query}. Find best practices.",
        expected_output="Research findings with recommended tools",
        agent=researcher,
        context=[plan_task]
    )

    code_task = Task(
        description=f"Write code for: {project_query}. Use research findings.",
        expected_output="Working code saved to files",
        agent=coder,
        context=[plan_task, research_task]
    )

    review_task = Task(
        description=f"Review the code. Check for issues and suggest improvements.",
        expected_output="Code review with improvement suggestions",
        agent=reviewer,
        context=[code_task]
    )

    # Create crew WITHOUT memory to reduce token usage
    crew = Crew(
        agents=[planner, researcher, coder, reviewer],
        tasks=[plan_task, research_task, code_task, review_task],
        verbose=True,
        memory=False  # Disabled to reduce token usage
    )
    
    return crew

def save_to_memory(result, project_query):
    """Save results to vector memory"""
    try:
        vector_memory = VectorMemory()
        vector_memory.add_document(
            f"Project: {project_query}",
            f"Completed development: {str(result)[:1000]}..."  # Truncate to save space
        )
        print("💾 Results saved to memory")
    except Exception as e:
        print(f"⚠️ Memory save failed: {e}")

def wait_for_rate_limit():
    """Wait function for rate limit resets"""
    print("⏳ Waiting for rate limit reset...")
    for i in range(30, 0, -5):
        print(f"   {i}s remaining...", end='\r')
        time.sleep(5)
    print("✅ Ready to continue")

def run_with_retry(crew, max_retries=2):
    """Run crew with automatic retry on rate limits"""
    
    for attempt in range(max_retries + 1):
        try:
            print(f"\n🚀 Starting development process (attempt {attempt + 1})...")
            result = crew.kickoff()
            return result
            
        except Exception as e:
            error_str = str(e).lower()
            
            if "rate_limit" in error_str or "rate limit" in error_str:
                if attempt < max_retries:
                    print(f"⚠️ Rate limit hit on attempt {attempt + 1}")
                    wait_for_rate_limit()
                    continue
                else:
                    print("❌ Max retries reached due to rate limits")
                    print("💡 Try again later or use a simpler version")
                    return None
            else:
                print(f"❌ Error: {e}")
                return None
    
    return None

def main():
    """Main function"""
    if not test_config():
        return
    
    project_query = get_project_query()
    
    print(f"\n📋 Project: {project_query}")
    print("🔄 Creating optimized development team...")
    
    crew = create_optimized_crew(project_query)
    
    print("\n🎯 Features enabled:")
    print("  ✅ Web search (Serper API)")
    print("  ✅ File operations")
    print("  ✅ Git integration")
    print("  ✅ Vector memory")
    print("  ⚡ Rate limit optimized")
    print("-" * 40)
    
    start_time = time.time()
    result = run_with_retry(crew)
    
    if result:
        end_time = time.time()
        print("\n" + "=" * 50)
        print("🎉 DEVELOPMENT COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"⏱️ Total time: {end_time - start_time:.1f} seconds")
        
        save_to_memory(result, project_query)
        
        print(f"\n📊 Summary:")
        print(f"  📝 Project: {project_query}")
        print(f"  ✅ Status: Completed")
        print(f"  💾 Results: Saved to memory")
        print("=" * 50)
        
        return result
    else:
        print("\n❌ Development failed")
        print("💡 Recommendations:")
        print("  • Try a simpler project description")
        print("  • Use main_simple.py for basic functionality")
        print("  • Wait a few minutes and try again")

if __name__ == "__main__":
    main()
