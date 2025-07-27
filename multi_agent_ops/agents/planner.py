from crewai import Agent
from memory.vector_store import VectorMemory
from config.llm_config import get_shared_llm

vector_memory = VectorMemory()

def save_to_vector_store(output):
    vector_memory.add(str(output), metadata={"agent": "Planner"})
    return output

class PlannerAgent:
    def build(self):
        try:
            # Get planning context from memory
            related_plans = vector_memory.search("project planning development steps", k=3)
            context = "\n".join([doc.page_content for doc in related_plans]) if related_plans else "No previous planning context available."
        except Exception as e:
            print(f"⚠️ Vector memory error in planner: {e}")
            context = "No previous planning context available."
        
        return Agent(
            role='Task Planner',
            goal='Break down the main goal into clear, achievable steps',
            backstory=(
                "You are an expert project planner who knows how to design efficient workflows. "
                "You create detailed, actionable development plans with clear steps and dependencies.\n\n"
                f"Previous planning context:\n{context}"
            ),
            llm=get_shared_llm(),
            allow_delegation=False,  # Disable delegation to avoid rate limits
            verbose=True,
            output_router=save_to_vector_store
        )
