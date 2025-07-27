from crewai import Crew, Task, Agent, LLM
from memory.vector_store import VectorMemory
import time
import os

from dotenv import load_dotenv
load_dotenv()

print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("DEBUG: OPENAI_API_BASE =", os.getenv("OPENAI_API_BASE"))
print("DEBUG: OPENAI_MODEL =", os.getenv("OPENAI_MODEL"))

# Initialize memory
vector_memory = VectorMemory()

# Configure LLM
llm = LLM(
    model=os.getenv("OPENAI_MODEL", "llama3-8b-8192"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# Simple agents without complex tools
planner = Agent(
    role='Task Planner',
    goal='Break down the main goal into clear, achievable steps',
    backstory="You are an expert project planner who knows how to design efficient workflows.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

coder = Agent(
    role='Python Developer',
    goal='Write clean, functional Python code',
    backstory="You are a top-tier Python engineer who writes clean, well-documented code.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

reviewer = Agent(
    role='Code Reviewer',
    goal='Evaluate the quality of outputs and recommend improvements',
    backstory="You're a meticulous reviewer who provides constructive feedback.",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# Define tasks with proper context passing
plan_task = Task(
    description="Break down the requirement to build a CLI To-Do app into actionable development steps.",
    expected_output="A detailed step-by-step development plan with clear subtasks.",
    agent=planner
)

code_task = Task(
    description="Use the planning to implement a basic CLI To-Do app in Python with add, list, and delete features.",
    expected_output="Python source code for the CLI app with clean structure, comments, and basic input validation.",
    agent=coder,
    context=[plan_task]  # Pass plan as context
)

review_task = Task(
    description="Review the code written for the CLI To-Do app. Suggest improvements or fixes if needed.",
    expected_output="A clear review with specific feedback or a pass approval.",
    agent=reviewer,
    context=[code_task]  # Pass code as context
)

# The Crew
crew = Crew(
    agents=[planner, coder, reviewer],
    tasks=[plan_task, code_task, review_task],
    verbose=True
)

# Run the crew and save results to memory
def run_with_memory():
    print("🚀 Starting multi-agent development process...")
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
