from crewai import Agent
from config.llm_config import get_shared_llm

class ReviewerAgent:
    def build(self):
        return Agent(
            role='Code Reviewer',
            goal='Evaluate the quality of outputs and recommend improvements',
            backstory=(
                "You're a meticulous and highly skeptical reviewer. "
                "You read other agents' work, point out flaws, and suggest clear, actionable improvements. "
                "You provide detailed feedback on code quality, structure, and best practices."
            ),
            llm=get_shared_llm(),
            allow_delegation=False,
            verbose=True
        )
