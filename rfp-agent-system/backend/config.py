"""Configuration settings for RFP Agent System"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Blob Storage (for document storage)
BLOB_CONN_STRING = os.getenv("BLOB_CONN_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "rfpenhancer1")

# Azure Document Intelligence (for PDF text extraction)
FORM_RECOGNIZER_ENDPOINT = os.getenv("FORM_RECOGNIZER_ENDPOINT")
FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")
