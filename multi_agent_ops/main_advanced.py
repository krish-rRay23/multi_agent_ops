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

print("🚀 Advanced Multi-Agent Development System")
print("🔥 Powered by Ollama - No Rate Limits!")
print("=" * 50)
print("📡 LLM: Ollama (localhost:11434)")
print("🧠 General Model: llama3.1:8b")
print("💻 Coding Model: qwen2.5-coder:7b")
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
    print("- CLI To-Do app with database")
    print("- Web scraper for news articles") 
    print("- Discord bot with commands")
    print("- REST API with FastAPI")
    print("- Data analysis tool")
    
    query = input("\n📝 Enter your project description: ").strip()
    if not query:
        return "CLI To-Do app with database and file persistence"
    return query

def create_advanced_crew(project_query):
    """Create crew with advanced configuration"""
    
    # Initialize agents with dynamic context
    planner = PlannerAgent().build()
    researcher = ResearcherAgent().build(query=project_query)
    coder = CoderAgent().build()
    reviewer = ReviewerAgent().build()

    # Define optimized tasks (shorter descriptions to reduce token usage)
    plan_task = Task(
        description=f"Create development plan for: {project_query}. Include key steps and dependencies.",
        expected_output="Development plan with clear steps and dependencies",
        agent=planner
    )

    research_task = Task(
        description=f"Research tools and libraries for: {project_query}. Find best practices and examples.",
        expected_output="Research findings with recommended tools and best practices",
        agent=researcher,
        context=[plan_task]
    )

    code_task = Task(
        description=f"Write code for: {project_query}. Use research findings and save to files.",
        expected_output="Working code saved to appropriate files",
        agent=coder,
        context=[plan_task, research_task]
    )

    review_task = Task(
        description=f"Review the code. Check for issues and suggest improvements.",
        expected_output="Code review with specific feedback and suggestions",
        agent=reviewer,
        context=[code_task]
    )

    # Create the crew (disable memory to reduce token usage)
    crew = Crew(
        agents=[planner, researcher, coder, reviewer],
        tasks=[plan_task, research_task, code_task, review_task],
        verbose=True,
        memory=False  # Disabled to avoid rate limits
    )
    
    return crew, [plan_task, research_task, code_task, review_task]

def save_results_to_memory(result, project_query):
    """Enhanced memory saving with better context"""
    try:
        vector_memory.add(
            text=f"Project: {project_query}\n\nComplete development process and results:\n{str(result)}",
            metadata={
                "project": project_query,
                "timestamp": str(int(time.time())),
                "status": "completed",
                "type": "full_project"
            }
        )
        print("✅ Results saved to memory for future reference")
    except Exception as e:
        print(f"⚠️ Could not save to memory: {e}")

def run_advanced_system():
    """Run the advanced multi-agent system"""
    
    # Get project requirements
    project_query = get_project_query()
    
    print(f"\n🔧 Creating development team for: {project_query}")
    
    # Create advanced crew
    crew, tasks = create_advanced_crew(project_query)
    
    print(f"\n🚀 Starting advanced multi-agent development process...")
    print(f"📋 Project: {project_query}")
    print("👥 Team: Planner → Researcher → Coder → Reviewer")
    print("🧠 Memory: Enabled with vector storage")
    print("🔍 Web Search: Enabled")
    print("📁 File Operations: Enabled")
    print("🐙 Git Integration: Enabled")
    print("-" * 60)
    
    try:
        # Execute the crew with rate limit handling
        print("🚀 Starting development process...")
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("🎉 DEVELOPMENT COMPLETE!")
        print("=" * 60)
        
        # Save results to memory
        save_results_to_memory(result, project_query)
        
        print(f"\n📊 Final Result Summary:")
        print(f"📝 Project: {project_query}")
        print(f"✅ Status: Completed successfully")
        print(f"🧠 Memory: Results saved for future projects")
        
        return result
        
    except Exception as e:
        error_str = str(e).lower()
        print(f"\n❌ Development process failed: {e}")
        
        if "rate_limit" in error_str or "rate limit" in error_str:
            print("💡 Rate limit exceeded. Recommendations:")
            print("  • Wait 1-2 minutes and try again")
            print("  • Use shorter project descriptions")
            print("  • Try main_simple.py for basic functionality")
        else:
            print("💡 Try running again or check your configuration")
        return None

if __name__ == "__main__":
    run_advanced_system()
