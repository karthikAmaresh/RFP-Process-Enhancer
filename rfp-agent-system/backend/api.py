"""
FastAPI server for RFP document processing
Provides REST API endpoints for the React frontend
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
from pathlib import Path
from pipeline import process_rfp_document

app = FastAPI(title="RFP Process Enhancer API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],  # Vite ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "RFP Process Enhancer API is running"}

@app.post("/api/process")
async def process_document(file: UploadFile = File(...), use_blob_storage: bool = True):
    """
    Process uploaded RFP document through the AI pipeline
    
    Args:
        file: PDF file uploaded by user
        use_blob_storage: If True, upload to Azure Blob Storage first (default: True)
        
    Returns:
        JSON with processing results and generated knowledge base
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    content = await file.read()
    blob_name = None
    tmp_path = None
    
    try:
        if use_blob_storage:
            # Upload to Azure Blob Storage
            from azure.storage.blob import BlobServiceClient
            import config
            from datetime import datetime
            
            if config.AZURE_STORAGE_CONNECTION_STRING:
                try:
                    print(f"Uploading {file.filename} to Azure Blob Storage...")
                    
                    blob_service_client = BlobServiceClient.from_connection_string(
                        config.AZURE_STORAGE_CONNECTION_STRING
                    )
                    container_name = "rfp-documents"
                    
                    # Create container if doesn't exist
                    try:
                        container_client = blob_service_client.get_container_client(container_name)
                        if not container_client.exists():
                            container_client.create_container()
                            print(f"✓ Created container: {container_name}")
                        else:
                            print(f"✓ Using existing container: {container_name}")
                    except Exception as e:
                        print(f"Container check/create error: {e}")
                        # Try to create anyway
                        try:
                            blob_service_client.create_container(container_name)
                            print(f"✓ Created container: {container_name}")
                        except:
                            pass  # Already exists
                    
                    # Generate unique blob name with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    blob_name = f"{timestamp}_{file.filename}"
                    
                    # Upload file
                    blob_client = blob_service_client.get_blob_client(
                        container=container_name,
                        blob=blob_name
                    )
                    blob_client.upload_blob(content, overwrite=True)
                    print(f"✓ Uploaded to blob: {blob_name}")
                    
                    # Process from blob
                    process_rfp_document(blob_name=blob_name)
                    
                except Exception as blob_error:
                    print(f"⚠ Blob storage error: {blob_error}")
                    print("⚠ Falling back to local processing...")
                    use_blob_storage = False
            else:
                print("⚠ Blob storage not configured, falling back to local processing")
                use_blob_storage = False
        
        if not use_blob_storage:
            # Create temporary file for local processing
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            # Process the document through the pipeline
            print(f"Processing document: {file.filename}")
            import traceback
            try:
                process_rfp_document(file_path=tmp_path)
            except Exception as pipeline_error:
                print(f"Pipeline error: {str(pipeline_error)}")
                print(traceback.format_exc())
                raise
        
        # Read the generated knowledge base
        kb_path = Path(__file__).parent / "kb.md"
        print(f"Looking for kb.md at: {kb_path}")
        if kb_path.exists():
            with open(kb_path, 'r', encoding='utf-8') as f:
                kb_content = f.read()
        else:
            kb_content = "Knowledge base file not found"
        
        return JSONResponse(content={
            "success": True,
            "message": f"Successfully processed {file.filename}",
            "filename": file.filename,
            "blob_name": blob_name if use_blob_storage else None,
            "storage_location": "Azure Blob Storage" if use_blob_storage else "Local",
            "output": kb_content
        })
        
    except Exception as e:
        import traceback
        error_detail = f"Processing failed: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    
    finally:
        # Clean up temporary file (only if using local processing)
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.get("/api/kb")
async def get_knowledge_base():
    """
    Retrieve the current knowledge base content
    
    Returns:
        JSON with the knowledge base markdown content
    """
    kb_path = Path(__file__).parent / "kb.md"
    
    if not kb_path.exists():
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    
    with open(kb_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return JSONResponse(content={
        "success": True,
        "content": content
    })

@app.get("/api/documents")
async def list_documents():
    """
    List all documents in Azure Blob Storage
    
    Returns:
        JSON with list of stored documents
    """
    try:
        from azure.storage.blob import BlobServiceClient
        import config
        
        if not config.AZURE_STORAGE_CONNECTION_STRING:
            return JSONResponse(content={
                "success": False,
                "message": "Blob storage not configured",
                "documents": []
            })
        
        blob_service_client = BlobServiceClient.from_connection_string(
            config.AZURE_STORAGE_CONNECTION_STRING
        )
        container_client = blob_service_client.get_container_client("rfp-documents")
        
        documents = []
        for blob in container_client.list_blobs():
            documents.append({
                "name": blob.name,
                "size": blob.size,
                "created": blob.creation_time.isoformat() if blob.creation_time else None,
                "last_modified": blob.last_modified.isoformat() if blob.last_modified else None
            })
        
        return JSONResponse(content={
            "success": True,
            "count": len(documents),
            "documents": documents
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.delete("/api/documents/{blob_name}")
async def delete_document(blob_name: str):
    """
    Delete a document from Azure Blob Storage
    
    Args:
        blob_name: Name of the blob to delete
    """
    try:
        from azure.storage.blob import BlobServiceClient
        import config
        
        if not config.AZURE_STORAGE_CONNECTION_STRING:
            raise HTTPException(status_code=400, detail="Blob storage not configured")
        
        blob_service_client = BlobServiceClient.from_connection_string(
            config.AZURE_STORAGE_CONNECTION_STRING
        )
        blob_client = blob_service_client.get_blob_client(
            container="rfp-documents",
            blob=blob_name
        )
        
        blob_client.delete_blob()
        
        return JSONResponse(content={
            "success": True,
            "message": f"Deleted {blob_name}"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting RFP Process Enhancer API server...")
    print("API documentation available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
