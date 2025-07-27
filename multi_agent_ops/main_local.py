from crewai import Crew, Task
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from memory.vector_store import VectorMemory
from config.llm_config import get_shared_llm, get_shared_coding_llm
import time
import os

print("🚀 LOCAL Multi-Agent Development System")
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
    coding_llm = get_shared_coding_llm()
    print("✅ General LLM: Successfully loaded (llama3.1:8b)")
    print("✅ Coding LLM: Successfully loaded (qwen2.5-coder:7b)")
except Exception as e:
    print(f"❌ LLM Configuration Error: {e}")
    print("💡 Make sure Ollama is running: ollama serve")
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

def create_local_crew(project_query):
    """Create crew optimized for local LLM usage"""
    
    print("🔧 Initializing AI agents...")
    
    # Initialize agents with local LLMs
    planner = PlannerAgent().build()
    researcher = ResearcherAgent().build(query=project_query)
    coder = CoderAgent().build()  # Uses coding-specialized model
    reviewer = ReviewerAgent().build()
    
    print("✅ Planner Agent: Ready (llama3.1:8b)")
    print("✅ Researcher Agent: Ready (llama3.1:8b + web search)")
    print("✅ Coder Agent: Ready (qwen2.5-coder:7b)")
    print("✅ Reviewer Agent: Ready (llama3.1:8b)")

    # Define tasks with clear outputs
    plan_task = Task(
        description=f"Create a comprehensive development plan for: {project_query}. Include key steps, dependencies, and technologies needed.",
        expected_output="Detailed development plan with clear steps and dependencies",
        agent=planner
    )

    research_task = Task(
        description=f"Research the best tools, libraries, and practices for: {project_query}. Find code examples and documentation.",
        expected_output="Research findings with recommended tools, libraries, and best practices",
        agent=researcher,
        context=[plan_task]
    )

    code_task = Task(
        description=f"Write complete, working code for: {project_query}. Use the research findings and development plan. Save code to appropriate files.",
        expected_output="Complete, functional code saved to files with proper structure",
        agent=coder,
        context=[plan_task, research_task]
    )

    review_task = Task(
        description=f"Review the generated code for: {project_query}. Check for bugs, improvements, and best practices. Provide specific feedback.",
        expected_output="Detailed code review with specific feedback and improvement suggestions",
        agent=reviewer,
        context=[code_task]
    )

    # Create the crew with local optimization
    crew = Crew(
        agents=[planner, researcher, coder, reviewer],
        tasks=[plan_task, research_task, code_task, review_task],
        verbose=True,
        memory=False  # Disabled for performance
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
                "type": "full_project",
                "llm": "ollama_local"
            }
        )
        print("✅ Results saved to memory for future reference")
    except Exception as e:
        print(f"⚠️ Could not save to memory: {e}")

def run_local_system():
    """Run the local multi-agent system with unlimited usage"""
    
    # Get project requirements
    project_query = get_project_query()
    
    print(f"\n🔧 Creating local development team for: {project_query}")
    
    # Create local crew
    crew, tasks = create_local_crew(project_query)
    
    print(f"\n🚀 Starting LOCAL multi-agent development process...")
    print(f"📋 Project: {project_query}")
    print("👥 Team: Planner → Researcher → Coder → Reviewer")
    print("🧠 Memory: Enabled with vector storage")
    print("🔍 Web Search: Enabled")
    print("📁 File Operations: Enabled")
    print("🐙 Git Integration: Enabled")
    print("🔥 Rate Limits: NONE (Local LLM)")
    print("-" * 60)
    
    try:
        # Execute the crew with unlimited local power
        print("🚀 Starting development process...")
        start_time = time.time()
        
        result = crew.kickoff()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        print("🎉 DEVELOPMENT COMPLETE!")
        print("=" * 60)
        
        # Save results to memory
        save_results_to_memory(result, project_query)
        
        print(f"\n📊 Final Result Summary:")
        print(f"📝 Project: {project_query}")
        print(f"✅ Status: Completed successfully")
        print(f"⏱️ Duration: {duration:.2f} seconds")
        print(f"🧠 Memory: Results saved for future projects")
        print(f"💰 Cost: $0.00 (Local LLM)")
        print(f"🔥 Rate Limits: None!")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Development process failed: {e}")
        print("💡 Troubleshooting:")
        print("  • Check if Ollama is running: ollama serve")
        print("  • Verify models are installed: ollama list")
        print("  • Check if CrewAI is installed: pip install crewai")
        return None

if __name__ == "__main__":
    run_local_system()
