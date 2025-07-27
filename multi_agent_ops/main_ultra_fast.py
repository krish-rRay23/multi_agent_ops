from crewai import Crew, Task
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent  
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
import time
import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.llm_config_fast import get_fast_llm

print("🚀 ULTRA-FAST Multi-Agent System")
print("⚡ Optimized for Maximum Speed!")
print("=" * 40)
print("📡 LLM: llama3.2:3b (2GB)")
print("⚡ Mode: LIGHTNING FAST")
print("=" * 40)

def get_project_query():
    """Get simple project requirements"""
    print("\n🎯 Quick project (keep it simple!):")
    print("Examples: calculator, file counter, password generator")
    
    query = input("\n📝 Project: ").strip()
    if not query:
        return "simple calculator"
    return query

def create_ultra_fast_crew(project_query):
    """Create minimal crew for maximum speed"""
    
    # Use fast LLM for all agents
    fast_llm = get_fast_llm()
    
    # Minimal agents
    planner = PlannerAgent().build()
    coder = CoderAgent().build()
    
    # Override with fast LLM
    planner.llm = fast_llm
    coder.llm = fast_llm

    # Minimal tasks
    plan_task = Task(
        description=f"Quick plan: {project_query}. Just list 3 steps.",
        expected_output="3 step plan",
        agent=planner
    )

    code_task = Task(
        description=f"Write simple working code for: {project_query}. One file, minimal code.",
        expected_output="Working Python code",
        agent=coder,
        context=[plan_task]
    )

    # Ultra-minimal crew
    crew = Crew(
        agents=[planner, coder],
        tasks=[plan_task, code_task],
        verbose=True,
        memory=False
    )
    
    return crew

def run_ultra_fast():
    """Run ultra-fast development"""
    
    project_query = get_project_query()
    
    print(f"\n⚡ Creating: {project_query}")
    print("👥 Team: Planner + Coder only")
    print("🚀 Starting in 3... 2... 1...")
    
    start_time = time.time()
    
    try:
        crew = create_ultra_fast_crew(project_query)
        result = crew.kickoff()
        
        duration = time.time() - start_time
        
        print(f"\n🎉 COMPLETED in {duration:.1f} seconds!")
        print("=" * 40)
        
        return result
        
    except Exception as e:
        print(f"\n❌ Failed: {e}")
        return None

if __name__ == "__main__":
    run_ultra_fast()
