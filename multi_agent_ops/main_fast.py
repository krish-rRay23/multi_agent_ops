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

print("🚀 FAST Multi-Agent Development System")
print("⚡ Powered by Ollama - Optimized for Speed!")
print("=" * 50)
print("📡 LLM: Ollama (localhost:11434)")
print("🧠 Fast Model: llama3.2:3b (2GB)")
print("💻 Coding Model: llama3.2:3b (shared)")
print("=" * 50)

# Initialize memory
vector_memory = VectorMemory()

# Test LLM configuration
try:
    llm = get_shared_llm()
    print("✅ LLM Configuration: Successfully loaded")
except Exception as e:
    print(f"❌ LLM Configuration Error: {e}")
    exit(1)

def get_project_query():
    """Get project requirements from user"""
    print("\n🎯 What would you like to build today?")
    print("Examples:")
    print("- CLI calculator")
    print("- Simple file organizer") 
    print("- Basic web scraper")
    print("- Data processor")
    print("- Utility script")
    
    query = input("\n📝 Enter your project description: ").strip()
    if not query:
        return "Simple CLI calculator with basic operations"
    return query

def create_fast_crew(project_query):
    """Create crew optimized for speed"""
    
    # Initialize agents with minimal context for speed
    planner = PlannerAgent().build()
    researcher = ResearcherAgent().build(query=project_query)
    coder = CoderAgent().build()
    reviewer = ReviewerAgent().build()

    # Define ultra-short tasks for speed
    plan_task = Task(
        description=f"Quick plan for: {project_query}. List 3-4 main steps only.",
        expected_output="Brief development plan",
        agent=planner
    )

    research_task = Task(
        description=f"Find 2-3 key libraries for: {project_query}. No web search - use knowledge.",
        expected_output="Library recommendations",
        agent=researcher,
        context=[plan_task]
    )

    code_task = Task(
        description=f"Write minimal working code for: {project_query}. Keep it simple and functional.",
        expected_output="Working code in one file",
        agent=coder,
        context=[plan_task, research_task]
    )

    review_task = Task(
        description=f"Quick review - check if code works and suggest 1-2 improvements.",
        expected_output="Brief code review",
        agent=reviewer,
        context=[code_task]
    )

    # Create the crew with speed optimizations
    crew = Crew(
        agents=[planner, researcher, coder, reviewer],
        tasks=[plan_task, research_task, code_task, review_task],
        verbose=True,
        memory=False,  # Disabled for speed
        max_execution_time=300  # 5 minute timeout
    )
    
    return crew, [plan_task, research_task, code_task, review_task]

def save_results_to_memory(result, project_query):
    """Save results to memory"""
    try:
        vector_memory.add(
            text=f"Fast Project: {project_query}\n\nResults:\n{str(result)}",
            metadata={
                "project": project_query,
                "timestamp": str(int(time.time())),
                "status": "completed",
                "type": "fast_project"
            }
        )
        print("✅ Results saved to memory")
    except Exception as e:
        print(f"⚠️ Could not save to memory: {e}")

def run_fast_system():
    """Run the optimized fast multi-agent system"""
    
    # Get project requirements
    project_query = get_project_query()
    
    print(f"\n⚡ Creating FAST development team for: {project_query}")
    
    # Create fast crew
    crew, tasks = create_fast_crew(project_query)
    
    print(f"\n🚀 Starting FAST development process...")
    print(f"📋 Project: {project_query}")
    print("👥 Team: Planner → Researcher → Coder → Reviewer")
    print("⚡ Mode: SPEED OPTIMIZED")
    print("🚫 Web Search: Disabled for speed")
    print("🧠 Memory: Minimal usage")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        # Execute the crew
        print("⚡ Starting FAST development...")
        result = crew.kickoff()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("🎉 FAST DEVELOPMENT COMPLETE!")
        print("=" * 60)
        
        # Save results to memory
        save_results_to_memory(result, project_query)
        
        print(f"\n📊 Final Result Summary:")
        print(f"📝 Project: {project_query}")
        print(f"✅ Status: Completed successfully")
        print(f"⚡ Duration: {duration:.1f} seconds")
        print(f"🧠 Memory: Results saved")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Fast development failed: {e}")
        print("💡 Try with an even simpler project description")
        return None

if __name__ == "__main__":
    run_fast_system()
