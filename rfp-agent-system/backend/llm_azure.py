"""Azure OpenAI LLM Client - Cloud-based AI for agent processing"""
from openai import AzureOpenAI
import os
from typing import Optional
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureOpenAIClient:
    """
    Azure OpenAI client for generating responses using GPT-4 or GPT-3.5.
    
    Features:
    - Automatic retry with exponential backoff
    - Token usage tracking
    - Cost estimation
    - Error handling
    """
    
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment_name: str,
        api_version: str = "2023-12-01-preview",
        max_retries: int = 3,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize Azure OpenAI client.
        
        Args:
            endpoint: Azure OpenAI endpoint URL
            api_key: Azure OpenAI API key
            deployment_name: Model deployment name (e.g., "gpt4-deployment")
            api_version: API version
            max_retries: Maximum retry attempts on failure
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
        """
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.deployment_name = deployment_name
        self.max_retries = max_retries
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Cost tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        
        # Pricing (per 1K tokens)
        # Update these based on your deployment model
        self.input_cost_per_1k = 0.03  # GPT-4: $0.03, GPT-3.5: $0.001
        self.output_cost_per_1k = 0.06  # GPT-4: $0.06, GPT-3.5: $0.002
        
        logger.info(f"Initialized Azure OpenAI client with deployment: {deployment_name}")
    
    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        Generate a response from Azure OpenAI.
        
        Args:
            prompt: User prompt/input
            system_message: Optional system message to set context
            
        Returns:
            str: Generated response text
        """
        messages = []
        
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        messages.append({"role": "user", "content": prompt})
        
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                
                response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=0.95,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                
                elapsed_time = time.time() - start_time
                
                # Extract response
                result = response.choices[0].message.content
                
                # Track usage
                usage = response.usage
                self.total_input_tokens += usage.prompt_tokens
                self.total_output_tokens += usage.completion_tokens
                
                # Calculate cost
                input_cost = (usage.prompt_tokens / 1000) * self.input_cost_per_1k
                output_cost = (usage.completion_tokens / 1000) * self.output_cost_per_1k
                call_cost = input_cost + output_cost
                self.total_cost += call_cost
                
                logger.info(
                    f"Azure OpenAI call completed - "
                    f"Time: {elapsed_time:.2f}s, "
                    f"Tokens: {usage.total_tokens} "
                    f"(in: {usage.prompt_tokens}, out: {usage.completion_tokens}), "
                    f"Cost: ${call_cost:.4f}"
                )
                
                return result
                
            except Exception as e:
                logger.error(f"Azure OpenAI error (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error("Max retries reached. Raising exception.")
                    raise
    
    def get_usage_stats(self) -> dict:
        """
        Get token usage and cost statistics.
        
        Returns:
            dict: Usage statistics
        """
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost_usd": round(self.total_cost, 4),
            "input_cost_per_1k": self.input_cost_per_1k,
            "output_cost_per_1k": self.output_cost_per_1k
        }
    
    def reset_stats(self):
        """Reset usage statistics."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        logger.info("Usage statistics reset")


def set_pricing_for_model(client: AzureOpenAIClient, model_name: str):
    """
    Set pricing based on model type.
    
    Args:
        client: AzureOpenAIClient instance
        model_name: Model name (gpt4, gpt35, gpt4o, etc.)
    """
    pricing_map = {
        "gpt4": (0.03, 0.06),
        "gpt-4": (0.03, 0.06),
        "gpt4o": (0.0025, 0.01),  # GPT-4o pricing
        "gpt-4o": (0.0025, 0.01),
        "gpt4-32k": (0.06, 0.12),
        "gpt-4-32k": (0.06, 0.12),
        "gpt35": (0.001, 0.002),
        "gpt-35-turbo": (0.001, 0.002),
        "gpt-35-turbo-16k": (0.001, 0.002),
    }
    
    model_key = model_name.lower()
    if model_key in pricing_map:
        client.input_cost_per_1k, client.output_cost_per_1k = pricing_map[model_key]
        logger.info(f"Set pricing for {model_name}: ${client.input_cost_per_1k}/1K in, ${client.output_cost_per_1k}/1K out")
    else:
        logger.warning(f"Unknown model {model_name}, using default pricing")


if __name__ == "__main__":
    # Test the Azure OpenAI client
    from config import (
        AZURE_OPENAI_ENDPOINT,
        AZURE_OPENAI_KEY,
        AZURE_OPENAI_DEPLOYMENT_GPT4,
        AZURE_OPENAI_API_VERSION
    )
    
    print("Testing Azure OpenAI connection...")
    
    try:
        client = AzureOpenAIClient(
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            deployment_name=AZURE_OPENAI_DEPLOYMENT_GPT4,
            api_version=AZURE_OPENAI_API_VERSION
        )
        
        set_pricing_for_model(client, "gpt4")
        
        # Test prompt
        test_prompt = "Say 'Hello from Azure OpenAI!' and confirm you're working correctly."
        
        print("\nSending test prompt...")
        response = client.generate(test_prompt)
        
        print("\n" + "="*60)
        print("RESPONSE:")
        print("="*60)
        print(response)
        print("="*60)
        
        # Print usage stats
        stats = client.get_usage_stats()
        print("\nUsage Statistics:")
        print(f"  Total Tokens: {stats['total_tokens']}")
        print(f"  Input Tokens: {stats['total_input_tokens']}")
        print(f"  Output Tokens: {stats['total_output_tokens']}")
        print(f"  Total Cost: ${stats['total_cost_usd']}")
        
        print("\n✓ Azure OpenAI connection successful!")
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        print("\nPlease check:")
        print("1. Azure OpenAI endpoint is correct")
        print("2. API key is valid")
        print("3. Deployment name exists")
        print("4. You have quota/permissions")
