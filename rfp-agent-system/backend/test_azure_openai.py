"""Test script to verify Azure OpenAI connection"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_client import LLMClient


def test_azure_openai():
    """Test Azure OpenAI connection and agent response"""
    
    print("="*60)
    print("Testing Azure OpenAI Connection")
    print("="*60)
    
    # Simple test prompt
    test_prompt = """You are a Senior Business Analyst testing the Azure OpenAI integration.

Please confirm:
1. You are receiving this message
2. You can generate responses
3. The connection is working

Respond with a brief confirmation message."""
    
    print("\nSending test prompt to Azure OpenAI...")
    print("-"*60)
    
    try:
        llm_client = LLMClient()
        response = llm_client.generate(test_prompt)
        
        print("\n✓ SUCCESS! Azure OpenAI Response:")
        print("-"*60)
        print(response)
        print("-"*60)
        
        # Get usage stats
        stats = llm_client.get_usage_stats()
        if "total_tokens" in stats:
            print("\n📊 Usage Statistics:")
            print(f"  Total Tokens: {stats['total_tokens']}")
            print(f"  Input Tokens: {stats['total_input_tokens']}")
            print(f"  Output Tokens: {stats['total_output_tokens']}")
            print(f"  Cost: ${stats['total_cost_usd']}")
        
        print("\n✓ Azure OpenAI integration is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nPlease check:")
        print("1. AZURE_OPENAI_ENDPOINT is set in .env file")
        print("2. AZURE_OPENAI_KEY is set in .env file")
        print("3. Deployment name matches (e.g., gpt4-deployment)")
        print("4. USE_AZURE_OPENAI=true in .env file")
        print("5. You have quota/permissions in Azure")
        return False


if __name__ == "__main__":
    test_azure_openai()
