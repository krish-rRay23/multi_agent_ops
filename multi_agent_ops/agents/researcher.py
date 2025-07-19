from crewai import Agent
from tools.web_search import web_search_tool

class ResearcherAgent:
    def build(self):
        return Agent(
            role='Technical Researcher',
            goal='Gather detailed, relevant technical information to support the task',
            backstory=(
                "You are a highly skilled technical researcher. "
                "You explore documentation, articles, and online resources to support the team with reliable insights."
            ),
            tools=[web_search_tool],  # ✅ Use the exported tool
            allow_delegation=False,
            verbose=True
        )
