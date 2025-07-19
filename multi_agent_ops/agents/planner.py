from crewai import Agent
from memory.memory_store import MemoryStore

# Shared instance (will be imported by others too)
memory = MemoryStore()

class PlannerAgent:
    def build(self):
        return Agent(
            role='Task Planner',
            goal='Break down the main goal into clear, achievable steps',
            backstory=(
                "You are an expert project planner who knows how to design efficient workflows. "
                "Your job is to take complex tasks and break them into actionable plans for the rest of the team."
            ),
            allow_delegation=True,
            verbose=True,
            output_router=lambda output: memory.save("plan", output)
        )
