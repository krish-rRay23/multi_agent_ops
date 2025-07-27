from crewai import Agent
from memory.memory_store import memory
from tools.file_writer import write_to_file
from tools.git_ops import git_commit_and_pr
from config.llm_config import get_shared_coding_llm

file_writer_tool = write_to_file  # correct binding

class CoderAgent:
    def build(self):
        planning_context = memory.retrieve("plan") or "No plan provided."

        return Agent(
            role='Python Developer',
            goal='Write clean, functional Python code, save it to a file, and commit it to GitHub.',
            backstory=(
                f"You are a top-tier Python engineer who writes clean, well-documented code. "
                f"You save your code to files and commit to GitHub repositories.\n\n"
                f"Your context from the planner:\n{planning_context}"
            ),
            llm=get_shared_coding_llm(),  # Using specialized coding model
            tools=[file_writer_tool, git_commit_and_pr],
            allow_delegation=False,
            verbose=True
        )