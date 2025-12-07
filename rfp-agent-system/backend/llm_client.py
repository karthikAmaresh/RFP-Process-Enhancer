"""LLM Client - Interface to local Ollama LLM"""
from ollama import Client


# Initialize Ollama client
client = Client()


def local_llm(prompt: str, model: str = "llama3") -> str:
    """
    Send prompt to local Ollama LLM and get response.
    
    Args:
        prompt: Input prompt for the LLM
        model: Model name (default: llama3)
        
    Returns:
        Generated text response
    """
    response = client.generate(model=model, prompt=prompt)
    return response['response']
