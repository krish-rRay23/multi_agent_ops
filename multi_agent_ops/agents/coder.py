from crewai import Agent
from memory.memory_store import memory
from tools.file_writer import write_to_file
from tools.git_ops import git_commit_and_pr  # ✅ Decorated tool function

file_writer_tool = write_to_file  # correct binding

class CoderAgent:
    def build(self):
        planning_context = memory.retrieve("plan") or "No plan provided."

        return Agent(
            role='Python Developer',
            goal='Write clean, functional Python code, save it to a file, and commit it to GitHub.',  # 👈 Updated goal
            backstory=(
                f"You are a top-tier Python engineer. Your context from the planner:\n\n{planning_context}"
            ),
            tools=[file_writer_tool, git_commit_and_pr],  # 👈 Include Git tool
            allow_delegation=False,
            verbose=True
        )