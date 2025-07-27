from crewai import Crew, Task
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent
from memory.vector_store import VectorMemory
import time

from dotenv import load_dotenv

load_dotenv()
import os
print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("DEBUG: OPENAI_API_BASE =", os.getenv("OPENAI_API_BASE"))
print("DEBUG: OPENAI_MODEL =", os.getenv("OPENAI_MODEL"))

# Initialize memory
vector_memory = VectorMemory()

# Initialize agents
planner = PlannerAgent().build()
researcher = ResearcherAgent().build()
coder = CoderAgent().build()
reviewer = ReviewerAgent().build()

# Define tasks with proper context passing
plan_task = Task(
    description="Break down the requirement to build a CLI To-Do app into actionable development steps.",
    expected_output="A detailed step-by-step development plan with clear subtasks.",
    agent=planner
)

research_task = Task(
    description="Research useful libraries and examples for implementing a CLI To-Do app in Python. Use the planning output as context.",
    expected_output="List of recommended tools, libraries, and coding references.",
    agent=researcher,
    context=[plan_task]  # Pass plan as context
)

code_task = Task(
    description="Use the planning and research to implement a basic CLI To-Do app in Python with add, list, and delete features.",
    expected_output="Python source code for the CLI app with clean structure, comments, and basic input validation.",
    agent=coder,
    context=[plan_task, research_task]  # Pass both as context
)

review_task = Task(
    description="Review the code written for the CLI To-Do app. Suggest improvements or fixes if needed.",
    expected_output="A clear review with specific feedback or a pass approval.",
    agent=reviewer,
    context=[code_task]  # Pass code as context
)

# The Crew
crew = Crew(
    agents=[planner, researcher, coder, reviewer],
    tasks=[plan_task, research_task, code_task, review_task],
    verbose=True
)

# Run the crew and save results to memory
def run_with_memory():
    print("� Starting multi-agent development process...")
    result = crew.kickoff()
    
    # Save results to vector memory for future use
    try:
        vector_memory.add(
            text=f"CLI To-Do app development plan and implementation: {str(result)}",
            metadata={"task": "CLI To-Do app", "timestamp": str(int(time.time()))}
        )
        print("✅ Results saved to memory for future reference")
    except Exception as e:
        print(f"⚠️ Could not save to memory: {e}")
    
    return result

# Run the crew
if __name__ == "__main__":
    run_with_memory()
