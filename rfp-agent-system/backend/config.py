"""Configuration settings for RFP Agent System"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Blob Storage (for document storage)
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING")
AZURE_STORAGE_CONNECTION_STRING = os.getenv("BLOB_CONN_STRING")  # Alias for consistency
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "rfpenhancer1")

# Azure Document Intelligence (for PDF text extraction)
FORM_RECOGNIZER_ENDPOINT = os.getenv("FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

# Model Deployment Names (as created in Azure Portal/Foundry)
AZURE_OPENAI_DEPLOYMENT_GPT4 = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT4", "gpt4-deployment")
AZURE_OPENAI_DEPLOYMENT_GPT35 = os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT35", "gpt35-deployment")

# Azure OpenAI is the primary LLM provider
USE_AZURE_OPENAI = os.getenv("USE_AZURE_OPENAI", "true").lower() == "true"

# Model Selection: "gpt4" for better quality, "gpt35" for faster/cheaper
AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL", "gpt4")
