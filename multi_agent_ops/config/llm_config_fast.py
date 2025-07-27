from crewai import LLM

def get_fast_llm():
    """Get the fast local LLM configuration"""
    return LLM(
        model="ollama/llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0.1,  # Lower temperature for faster processing
        max_tokens=500,   # Smaller responses for speed
    )

def get_shared_llm():
    """Get shared LLM - fallback to fast model"""
    return get_fast_llm()

def get_shared_coding_llm():
    """Get coding LLM - use fast model for speed"""
    return LLM(
        model="ollama/llama3.2:3b",
        base_url="http://localhost:11434", 
        temperature=0.0,  # Deterministic for coding
        max_tokens=800,   # Slightly more for code
    )

# For backwards compatibility
def get_general_llm():
    return get_fast_llm()

def get_coding_llm():
    return get_shared_coding_llm()
