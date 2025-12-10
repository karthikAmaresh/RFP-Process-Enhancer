"""LLM Client - Interface to Azure OpenAI"""
import config
from llm_azure import AzureOpenAIClient, set_pricing_for_model


class LLMClient:
    """
    Azure OpenAI client for all AI agent operations.
    Uses GPT-4o for high-quality RFP analysis.
    """
    
    def __init__(self):
        # Initialize Azure OpenAI
        deployment_name = (
            config.AZURE_OPENAI_DEPLOYMENT_GPT4 
            if config.AZURE_OPENAI_MODEL in ["gpt4", "gpt-4o", "gpt4o"]
            else config.AZURE_OPENAI_DEPLOYMENT_GPT35
        )
        
        self.azure_client = AzureOpenAIClient(
            endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_key=config.AZURE_OPENAI_KEY,
            deployment_name=deployment_name,
            api_version=config.AZURE_OPENAI_API_VERSION,
            temperature=0.7,
            max_tokens=2000
        )
        
        # Set pricing based on model
        set_pricing_for_model(self.azure_client, config.AZURE_OPENAI_MODEL)
        
        print(f"✓ Initialized Azure OpenAI with {config.AZURE_OPENAI_MODEL}")
    
    def generate(self, prompt: str, model: str = None) -> str:
        """
        Generate response from Azure OpenAI.
        
        Args:
            prompt: Input prompt
            model: Ignored (kept for compatibility)
            
        Returns:
            Generated text response
        """
        return self.azure_client.generate(prompt)
    
    def get_usage_stats(self) -> dict:
        """
        Get usage statistics from Azure OpenAI.
        
        Returns:
            dict: Token usage and cost statistics
        """
        return self.azure_client.get_usage_stats()
