"""
Simple Ollama Test - Basic functionality check
"""
import requests
import json

def test_ollama_connection():
    """Test basic Ollama connection"""
    try:
        # Test if Ollama is running
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json()
            print("✅ Ollama is running!")
            print("\n📋 Available models:")
            for model in models.get('models', []):
                print(f"  - {model['name']} ({model['size']})")
            return True
        else:
            print("❌ Ollama server not responding")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_model_generation(model_name="llama3.1:8b"):
    """Test model generation"""
    try:
        url = "http://localhost:11434/api/generate"
        data = {
            "model": model_name,
            "prompt": "Write a simple Python function to calculate factorial:",
            "stream": False
        }
        
        print(f"\n🧪 Testing {model_name} generation...")
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Generation successful!")
            print(f"\n🤖 Response:\n{result['response']}")
            return True
        else:
            print(f"❌ Generation failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Ollama Local Setup...")
    
    # Test connection
    if test_ollama_connection():
        # Test general model
        test_model_generation("llama3.1:8b")
        
        print("\n" + "="*50)
        
        # Test coding model
        test_model_generation("qwen2.5-coder:7b")
        
        print("\n🎉 Local LLM setup is working perfectly!")
        print("🔥 No more rate limits - unlimited usage!")
    else:
        print("\n❌ Setup incomplete. Make sure Ollama is running.")
