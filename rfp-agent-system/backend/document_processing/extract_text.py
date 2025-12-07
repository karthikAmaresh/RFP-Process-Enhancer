# Text extraction from RFP documents
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """
    Extract text from PDF document bytes using Azure Form Recognizer
    Works with private blob storage
    
    Args:
        file_bytes: PDF file content as bytes
        
    Returns:
        str: Extracted text content from the document
    """
    if not config.FORM_RECOGNIZER_ENDPOINT or not config.FORM_RECOGNIZER_KEY:
        raise ValueError("Azure Form Recognizer credentials not configured")
        
    client = DocumentAnalysisClient(
        endpoint=config.FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(config.FORM_RECOGNIZER_KEY)
    )
    
    # Analyze from bytes instead of URL (works with private blob storage)
    poller = client.begin_analyze_document("prebuilt-read", file_bytes)
    result = poller.result()
    
    # Extract all text content
    full_text = "\n".join([
        line.content 
        for page in result.pages 
        for line in page.lines
    ])
    
    return full_text


def extract_text_from_pdf(file_url: str) -> str:
    """
    Extract text from PDF document using Azure Form Recognizer (URL method)
    Note: This doesn't work with private blob storage
    
    Args:
        file_url: URL of the PDF document
        
    Returns:
        str: Extracted text content from the document
    """
    if not config.FORM_RECOGNIZER_ENDPOINT or not config.FORM_RECOGNIZER_KEY:
        raise ValueError("Azure Form Recognizer credentials not configured")
        
    client = DocumentAnalysisClient(
        endpoint=config.FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(config.FORM_RECOGNIZER_KEY)
    )
    
    poller = client.begin_analyze_document_from_url("prebuilt-read", file_url)
    result = poller.result()
    
    # Extract all text content
    full_text = "\n".join([
        line.content 
        for page in result.pages 
        for line in page.lines
    ])
    
    return full_text


def extract_text_from_blob(blob_name: str) -> str:
    """
    Extract text from a document stored in Azure Blob Storage
    Works with private blob storage by downloading and analyzing bytes
    
    Args:
        blob_name: Name of the blob file in storage
        
    Returns:
        str: Extracted text content from the document
    """
    if not config.BLOB_CONN_STRING:
        raise ValueError("Azure Blob Storage connection string not configured")
        
    # Download blob content as bytes
    blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONN_STRING)
    container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
    blob_client = container_client.get_blob_client(blob_name)
    
    # Download the blob content
    blob_data = blob_client.download_blob()
    file_bytes = blob_data.readall()
    
    # Extract text from bytes (works with private blob storage)
    return extract_text_from_pdf_bytes(file_bytes)


def extract_text_with_structure(file_url: str) -> dict:
    """
    Extract text with structural information (tables, paragraphs, etc.)
    
    Args:
        file_url: URL of the document
        
    Returns:
        dict: Structured document content including text, tables, and metadata
    """
    if not config.FORM_RECOGNIZER_ENDPOINT or not config.FORM_RECOGNIZER_KEY:
        raise ValueError("Azure Form Recognizer credentials not configured")
        
    client = DocumentAnalysisClient(
        endpoint=config.FORM_RECOGNIZER_ENDPOINT,
        credential=AzureKeyCredential(config.FORM_RECOGNIZER_KEY)
    )
    
    poller = client.begin_analyze_document_from_url("prebuilt-layout", file_url)
    result = poller.result()
    
    extracted_data = {
        "text": "",
        "tables": [],
        "paragraphs": [],
        "page_count": len(result.pages)
    }
    
    # Extract paragraphs
    if result.paragraphs:
        extracted_data["paragraphs"] = [p.content for p in result.paragraphs]
        extracted_data["text"] = "\n\n".join(extracted_data["paragraphs"])
    
    # Extract tables
    if result.tables:
        for table in result.tables:
            table_data = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": [
                    {
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "content": cell.content
                    }
                    for cell in table.cells
                ]
            }
            extracted_data["tables"].append(table_data)
    
    return extracted_data
