import os
from crewai import LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_llm():
    """
    Get configured LLM instance for all agents
    This centralizes LLM configuration so we don't repeat it everywhere
    Now using Ollama for unlimited local usage!
    """
    return LLM(
        model="ollama/llama3.1:8b",
        base_url="http://localhost:11434"
    )

def get_coding_llm():
    """
    Get coding-focused LLM for better code generation
    """
    return LLM(
        model="ollama/qwen2.5-coder:7b",
        base_url="http://localhost:11434"
    )

# Create singleton instances
_llm_instance = None
_coding_llm_instance = None

def get_shared_llm():
    """Get shared LLM instance (singleton pattern)"""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = get_llm()
    return _llm_instance

def get_shared_coding_llm():
    """Get shared coding LLM instance (singleton pattern)"""
    global _coding_llm_instance
    if _coding_llm_instance is None:
        _coding_llm_instance = get_coding_llm()
    return _coding_llm_instance
