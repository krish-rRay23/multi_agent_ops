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

print("🚀 Streamlined Multi-Agent Development System")
print("=" * 50)
print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY")[:20] + "..." if os.getenv("OPENAI_API_KEY") else "Not set")
print("DEBUG: OPENAI_API_BASE =", os.getenv("OPENAI_API_BASE"))
print("DEBUG: OPENAI_MODEL =", os.getenv("OPENAI_MODEL"))
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

def create_streamlined_crew(project_query):
    """Create crew with streamlined configuration to avoid rate limits"""
    
    # Initialize agents with dynamic context
    planner = PlannerAgent().build()
    researcher = ResearcherAgent().build(query=project_query)
    coder = CoderAgent().build()
    reviewer = ReviewerAgent().build()

    # Define streamlined tasks with shorter descriptions
    plan_task = Task(
        description=f"Create a development plan for: {project_query}. Include key steps and dependencies.",
        expected_output="A step-by-step development plan with clear tasks and dependencies.",
        agent=planner
    )

    research_task = Task(
        description=f"Research tools and libraries for: {project_query}. Find best practices and examples.",
        expected_output="Research report with recommended tools, libraries, and implementation strategies.",
        agent=researcher,
        context=[plan_task]
    )

    code_task = Task(
        description=f"Implement {project_query} using the plan and research. Write clean, functional code.",
        expected_output="Complete, functional codebase with proper structure and documentation.",
        agent=coder,
        context=[plan_task, research_task]
    )

    review_task = Task(
        description=f"Review the {project_query} implementation. Check for bugs and suggest improvements.",
        expected_output="Code review with specific feedback and improvement suggestions.",
        agent=reviewer,
        context=[code_task]
    )

    # Create the streamlined crew (without memory to reduce token usage)
    crew = Crew(
        agents=[planner, researcher, coder, reviewer],
        tasks=[plan_task, research_task, code_task, review_task],
        verbose=True,
        memory=False  # Disable crew memory to reduce token usage
    )
    
    return crew, [plan_task, research_task, code_task, review_task]

def save_results_to_memory(result, project_query):
    """Enhanced memory saving with better context"""
    try:
        vector_memory.add(
            text=f"Project: {project_query}\n\nResults: {str(result)[:2000]}",  # Limit text length
            metadata={
                "project": project_query,
                "timestamp": str(int(time.time())),
                "status": "completed",
                "type": "streamlined_project"
            }
        )
        print("✅ Results saved to memory for future reference")
    except Exception as e:
        print(f"⚠️ Could not save to memory: {e}")

def run_streamlined_system():
    """Run the streamlined multi-agent system"""
    
    # Get project requirements
    project_query = get_project_query()
    
    print(f"\n🔧 Creating development team for: {project_query}")
    
    # Create streamlined crew
    crew, tasks = create_streamlined_crew(project_query)
    
    print(f"\n🚀 Starting streamlined multi-agent development process...")
    print(f"📋 Project: {project_query}")
    print("👥 Team: Planner → Researcher → Coder → Reviewer")
    print("🧠 Memory: Vector storage enabled")
    print("🔍 Web Search: Enabled") 
    print("📁 File Operations: Enabled")
    print("⚡ Mode: Rate-limit optimized")
    print("-" * 60)
    
    try:
        # Execute the crew
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
        print(f"\n❌ Development process failed: {e}")
        print("💡 Try running the simple version: python main_simple.py")
        return None

if __name__ == "__main__":
    run_streamlined_system()
