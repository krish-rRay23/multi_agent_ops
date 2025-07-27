"""
Local LLM Setup Guide - Ollama Configuration
"""

# 1. Download and install Ollama from: https://ollama.ai/
# 2. Install a model (run in terminal):
#    ollama pull llama3.1:8b
#    ollama pull codellama:7b
#    ollama pull qwen2.5-coder:7b

# 3. Start Ollama server:
#    ollama serve

# 4. Test it works:
#    ollama run llama3.1:8b "Hello, how are you?"

# Configuration for CrewAI with Ollama:
import os
from crewai import LLM

def get_ollama_llm(model="llama3.1:8b"):
    """Get Ollama LLM configuration"""
    return LLM(
        model=f"ollama/{model}",
        base_url="http://localhost:11434"
    )

def get_general_llm():
    """Get the general purpose model (llama3.1:8b)"""
    return get_ollama_llm("llama3.1:8b")

def get_coding_llm():
    """Get the coding-focused model (qwen2.5-coder:7b)"""
    return get_ollama_llm("qwen2.5-coder:7b")

# Usage examples:
# llm = get_general_llm()  # For planning, research, reviewing
# coding_llm = get_coding_llm()  # For code generation

# Test local connection:
if __name__ == "__main__":
    print("Testing Ollama connection...")
    try:
        test_llm = get_general_llm()
        print("✅ Ollama configuration ready!")
        print(f"✅ General model: llama3.1:8b")
        print(f"✅ Coding model: qwen2.5-coder:7b")
        print(f"✅ Base URL: http://localhost:11434")
    except Exception as e:
        print(f"❌ Error: {e}")
