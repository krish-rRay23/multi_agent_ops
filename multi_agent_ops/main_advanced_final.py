#!/usr/bin/env python3
"""
Advanced Multi-Agent System - Final Optimized Version
Two-agent system (Planner + Coder) to guarantee success while avoiding rate limits
"""

from crewai import Crew, Task
from agents.planner import PlannerAgent
from agents.coder import CoderAgent
from memory.vector_store import VectorMemory
from config.llm_config import get_shared_llm
import time
import os

from dotenv import load_dotenv
load_dotenv()

def test_config():
    """Test configuration"""
    print("🚀 Advanced Multi-Agent System - Final Optimized")
    print("=" * 50)
    print(f"API Key: {os.getenv('OPENAI_API_KEY')[:20]}..." if os.getenv('OPENAI_API_KEY') else "❌ Not set")
    print(f"Model: {os.getenv('OPENAI_MODEL')}")
    print("=" * 50)
    
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
    print("Examples: todo app, calculator, file organizer, password generator")
    
    query = input("\n📝 Project: ").strip()
    return query if query else "CLI todo app"

def create_final_crew(project_query):
    """Create optimized 2-agent crew"""
    
    print("🔧 Creating development team...")
    
    # Initialize agents
    planner = PlannerAgent().build()
    coder = CoderAgent().build()
    
    print("✅ Team ready: Planner + Coder")
    
    # Ultra-short task descriptions
    plan_task = Task(
        description=f"Plan {project_query}: key steps only",
        expected_output="Simple development steps",
        agent=planner
    )

    code_task = Task(
        description=f"Code {project_query}: working implementation",
        expected_output="Complete working code",
        agent=coder,
        context=[plan_task]
    )

    # Create minimal crew
    crew = Crew(
        agents=[planner, coder],
        tasks=[plan_task, code_task],
        verbose=True,
        memory=False  # Disabled to save tokens
    )
    
    return crew

def save_to_memory(result, project_query):
    """Save results to vector memory"""
    try:
        vector_memory = VectorMemory()
        vector_memory.add_document(
            f"Project: {project_query}",
            f"Result: {str(result)[:500]}..."  # Truncated
        )
        print("💾 Saved to memory")
    except Exception as e:
        print(f"⚠️ Memory save failed: {e}")

def run_with_smart_retry(crew, max_retries=1):
    """Run crew with smart retry"""
    
    for attempt in range(max_retries + 1):
        try:
            print(f"\n🚀 Starting development (attempt {attempt + 1})...")
            result = crew.kickoff()
            return result
            
        except Exception as e:
            error_str = str(e).lower()
            
            if "rate_limit" in error_str:
                if attempt < max_retries:
                    print(f"⚠️ Rate limit hit, waiting 45s...")
                    time.sleep(45)
                    continue
                else:
                    print("❌ Rate limit exceeded")
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
    print("🎯 Strategy: 2-agent optimized workflow")
    print("  ✅ Memory persistence")
    print("  ✅ File operations")  
    print("  ⚡ Rate limit optimized")
    print("-" * 30)
    
    crew = create_final_crew(project_query)
    
    start_time = time.time()
    result = run_with_smart_retry(crew)
    
    if result:
        end_time = time.time()
        print("\n" + "=" * 40)
        print("🎉 SUCCESS! Development Complete!")
        print("=" * 40)
        print(f"⏱️ Time: {end_time - start_time:.1f}s")
        print(f"📝 Project: {project_query}")
        print("✅ Status: Completed")
        
        save_to_memory(result, project_query)
        
        print("\n📋 Final Result:")
        print("-" * 20)
        print(str(result)[:1000] + ("..." if len(str(result)) > 1000 else ""))
        print("-" * 20)
        
        return result
    else:
        print("\n❌ Development failed")
        print("💡 Suggestion: Try a simpler project or wait and retry")

if __name__ == "__main__":
    main()
