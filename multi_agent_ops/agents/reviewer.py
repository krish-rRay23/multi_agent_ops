from crewai import Agent

class ReviewerAgent:
    def build(self):
        return Agent(
            role='Code Reviewer',
            goal='Evaluate the quality of outputs and recommend improvements',
            backstory=(
                "You're a meticulous and highly skeptical reviewer. "
                "You read other agents' work, point out flaws, and suggest clear, actionable improvements."
            ),
            allow_delegation=False,
            verbose=True
        )
