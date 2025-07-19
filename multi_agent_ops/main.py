from crewai import Crew, Task
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from agents.reviewer import ReviewerAgent

from dotenv import load_dotenv

load_dotenv()

# Initialize agents
planner = PlannerAgent().build()
researcher = ResearcherAgent().build()
coder = CoderAgent().build()
reviewer = ReviewerAgent().build()

# Define tasks
plan_task = Task(
    description="Break down the requirement to build a CLI To-Do app into actionable development steps.",
    expected_output="A detailed step-by-step development plan with clear subtasks.",
    agent=planner
)

research_task = Task(
    description="Research useful libraries and examples for implementing a CLI To-Do app in Python.",
    expected_output="List of recommended tools, libraries, and coding references.",
    agent=researcher
)

code_task = Task(
    description="Use the planning and research to implement a basic CLI To-Do app in Python with add, list, and delete features.",
    expected_output="Python source code for the CLI app with clean structure, comments, and basic input validation.",
    agent=coder,
    callback=lambda output: review_logic(output)
)

review_task = Task(
    description="Review the code written for the CLI To-Do app. Suggest improvements or fixes if needed.",
    expected_output="A clear review with specific feedback or a pass approval.",
    agent=reviewer
)

def review_logic(output):
    # Safely extract output string
    output_str = (
        str(output)
        if isinstance(output, str)
        else str(getattr(output, "response", output))
    )

    if any(word in output_str.lower() for word in ["improvement", "fix", "issue"]):
        print("🔁 Detected critique. Rebuilding code task with feedback...")

        updated_code_task = Task(
            description="Update the CLI To-Do app based on the following reviewer feedback:\n\n" + output_str,
            expected_output="An improved version of the CLI app code with the issues fixed.",
            agent=coder
        )

        retry_output = updated_code_task.execute()
        print("✅ Retry Completed.")
        return retry_output

    print("✅ Review Passed. No retry needed.")
    return output_str
 
#The Creww
crew = Crew(
    agents=[planner, researcher, coder, reviewer],
    tasks=[plan_task, research_task, code_task, review_task],
    verbose=True
)

# Run the crew
crew.kickoff()
