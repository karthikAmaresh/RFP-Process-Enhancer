# Configuration settings for the RFP Agent System
import os
from dotenv import load_dotenv

load_dotenv()

# Azure Blob Storage Configuration
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING") or os.getenv("AZURE_BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "rfp-documents")

# Azure Form Recognizer Configuration
FORM_RECOGNIZER_ENDPOINT = os.getenv("FORM_RECOGNIZER_ENDPOINT") or os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY") or os.getenv("AZURE_FORM_RECOGNIZER_KEY")

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Azure Cognitive Search Configuration
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME", "rfp-index")

# MongoDB Configuration
MONGO_CONN_STR = os.getenv("MONGO_CONN_STR")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "rfp_db")
