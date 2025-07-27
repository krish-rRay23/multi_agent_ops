from crewai import Agent
from tools.web_search import web_search_tool
from memory.vector_store import VectorMemory
from config.llm_config import get_shared_llm

class ResearcherAgent:
    def build(self, query="CLI To-Do app"):
        try:
            vector_memory = VectorMemory()
            related_plans = vector_memory.search(query, k=3)
            context = "\n".join([doc.page_content for doc in related_plans]) if related_plans else "No related plans found."
        except Exception as e:
            print(f"⚠️ Vector memory error: {e}")
            context = "No related plans found."
        
        return Agent(
            role='Technical Researcher',
            goal='Gather detailed, relevant technical information to support the task',
            backstory=(
                "You're a technical researcher who assists with accurate insights and examples. "
                "You search the web for current best practices, libraries, and code examples. "
                "You provide comprehensive research with links, examples, and recommendations.\n\n"
                f"Here's relevant memory from past plans:\n{context}"
            ),
            llm=get_shared_llm(),
            tools=[web_search_tool],
            allow_delegation=False,
            verbose=True
        )