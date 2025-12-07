# Main entry point for the RFP Agent System backend
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from azure.storage.blob import BlobServiceClient
import config
import uvicorn
from document_processing.extract_text import extract_text_from_blob, extract_text_with_structure, extract_text_from_pdf
from document_processing.chunking import chunk_text
from document_processing.embedding import embed
from document_processing.indexer import index_chunk
from process_rfp import process_rfp, process_rfp_from_blob

app = FastAPI(title="RFP Process Enhancer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Azure Blob Service Client (optional)
blob_service_client = None
if config.BLOB_CONN_STRING:
    try:
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_CONN_STRING)
    except Exception as e:
        print(f"Warning: Could not initialize Azure Blob Storage client: {e}")


@app.get("/")
async def root():
    return {"message": "RFP Process Enhancer API is running"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """
    Upload RFP document and process it end-to-end:
    1. Upload to Blob Storage
    2. Extract text
    3. Chunk text
    4. Generate embeddings
    5. Index in Azure Cognitive Search
    
    Args:
        file: The RFP document file to upload
        
    Returns:
        dict: Processing status and statistics
    """
    try:
        # Validate file type
        allowed_extensions = [".pdf", ".docx", ".doc", ".txt"]
        file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Step 1: Upload to blob storage
        file_name = upload_to_blob(file)
        
        # Step 2: Get blob URL and extract text
        container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(file_name)
        file_url = blob_client.url
        
        text = extract_text_from_pdf(file_url)
        
        # Step 3: Chunk the text
        chunks = chunk_text(text)
        
        # Step 4 & 5: Embed and index each chunk
        for i, chunk in enumerate(chunks):
            emb = embed(chunk)
            index_chunk(chunk, emb, file_name, i)
        
        return {
            "status": "indexed",
            "filename": file_name,
            "chunks": len(chunks),
            "text_length": len(text)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/process-rfp")
async def process_uploaded_rfp(file: UploadFile = File(...), storage: str = "both"):
    """
    Simplified RFP processing using the unified process_rfp module
    
    Args:
        file: The RFP document file to upload
        storage: Where to store - "mongo", "search", or "both" (default)
        
    Returns:
        dict: Processing status and statistics
    """
    try:
        # Validate file type
        allowed_extensions = [".pdf", ".docx", ".doc", ".txt"]
        file_ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Upload to blob storage
        file_name = upload_to_blob(file)
        
        # Process using unified module
        result = process_rfp_from_blob(file_name, storage=storage)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/extract-text/{filename}")
async def extract_text(filename: str):
    """
    Extract text from an uploaded RFP document
    
    Args:
        filename: Name of the file in blob storage
        
    Returns:
        dict: Extracted text content
    """
    try:
        text = extract_text_from_blob(filename)
        
        return {
            "status": "success",
            "filename": filename,
            "text": text,
            "text_length": len(text)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")


@app.post("/extract-structured/{filename}")
async def extract_structured(filename: str):
    """
    Extract structured content (text, tables, paragraphs) from RFP document
    
    Args:
        filename: Name of the file in blob storage
        
    Returns:
        dict: Structured document content
    """
    try:
        # Get blob URL
        container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
        blob_client = container_client.get_blob_client(filename)
        blob_url = blob_client.url
        
        # Extract structured content
        structured_data = extract_text_with_structure(blob_url)
        
        return {
            "status": "success",
            "filename": filename,
            "data": structured_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Structured extraction failed: {str(e)}")


def upload_to_blob(file: UploadFile) -> str:
    """
    Upload file to Azure Blob Storage
    
    Args:
        file: The file to upload
        
    Returns:
        str: The filename of the uploaded blob
    """
    container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
    
    # Create container if it doesn't exist
    try:
        container_client.create_container()
    except Exception:
        pass  # Container already exists
    
    # Upload blob
    blob_client = container_client.get_blob_client(file.filename)
    blob_client.upload_blob(file.file, overwrite=True)
    
    return file.filename


@app.get("/health")
async def health_check():
    """
    Health check endpoint to validate all services are configured
    """
    health_status = {
        "api": "healthy",
        "services": {}
    }
    
    # Check Azure Blob Storage
    try:
        blob_service_client.get_service_properties()
        health_status["services"]["blob_storage"] = "connected"
    except Exception as e:
        health_status["services"]["blob_storage"] = f"error: {str(e)}"
    
    # Check Azure Form Recognizer
    try:
        if config.FORM_RECOGNIZER_ENDPOINT and config.FORM_RECOGNIZER_KEY:
            health_status["services"]["form_recognizer"] = "configured"
        else:
            health_status["services"]["form_recognizer"] = "not configured"
    except Exception as e:
        health_status["services"]["form_recognizer"] = f"error: {str(e)}"
    
    # Check Azure OpenAI
    try:
        if config.AZURE_OPENAI_ENDPOINT and config.AZURE_OPENAI_API_KEY:
            health_status["services"]["azure_openai"] = "configured"
        else:
            health_status["services"]["azure_openai"] = "not configured"
    except Exception as e:
        health_status["services"]["azure_openai"] = f"error: {str(e)}"
    
    # Check Azure Search
    try:
        if config.SEARCH_ENDPOINT and config.SEARCH_API_KEY:
            health_status["services"]["azure_search"] = "configured"
        else:
            health_status["services"]["azure_search"] = "not configured"
    except Exception as e:
        health_status["services"]["azure_search"] = f"error: {str(e)}"
    
    # Check embedding model
    try:
        from document_processing.embedding import get_model_info
        model_info = get_model_info()
        health_status["services"]["embedding_model"] = model_info
    except Exception as e:
        health_status["services"]["embedding_model"] = f"error: {str(e)}"
    
    return health_status


@app.post("/validate-pipeline")
async def validate_pipeline():
    """
    Validate the entire pipeline without uploading a real document
    Tests each component of the processing pipeline
    """
    results = {
        "pipeline": "validation",
        "steps": []
    }
    
    # Step 1: Test text chunking
    try:
        from document_processing.chunking import chunk_text
        test_text = "This is a test sentence. " * 100
        chunks = chunk_text(test_text, size=50)
        results["steps"].append({
            "step": "1. Text Chunking",
            "status": "success",
            "details": f"Created {len(chunks)} chunks"
        })
    except Exception as e:
        results["steps"].append({
            "step": "1. Text Chunking",
            "status": "failed",
            "error": str(e)
        })
    
    # Step 2: Test embedding
    try:
        from document_processing.embedding import embed, get_model_info
        test_embedding = embed("Test text for embedding")
        model_info = get_model_info()
        results["steps"].append({
            "step": "2. Embedding Generation",
            "status": "success",
            "details": f"Embedding dimension: {len(test_embedding)}, Model: {model_info['model_name']}"
        })
    except Exception as e:
        results["steps"].append({
            "step": "2. Embedding Generation",
            "status": "failed",
            "error": str(e)
        })
    
    # Step 3: Test search client connection
    try:
        from document_processing.indexer import search_client
        results["steps"].append({
            "step": "3. Search Index Connection",
            "status": "success",
            "details": f"Connected to index: {config.SEARCH_INDEX_NAME}"
        })
    except Exception as e:
        results["steps"].append({
            "step": "3. Search Index Connection",
            "status": "failed",
            "error": str(e)
        })
    
    # Step 4: Test blob storage
    try:
        container_client = blob_service_client.get_container_client(config.BLOB_CONTAINER_NAME)
        results["steps"].append({
            "step": "4. Blob Storage Connection",
            "status": "success",
            "details": f"Container: {config.BLOB_CONTAINER_NAME}"
        })
    except Exception as e:
        results["steps"].append({
            "step": "4. Blob Storage Connection",
            "status": "failed",
            "error": str(e)
        })
    
    # Overall status
    failed_steps = [s for s in results["steps"] if s["status"] == "failed"]
    results["overall_status"] = "failed" if failed_steps else "success"
    results["summary"] = f"{len(results['steps']) - len(failed_steps)}/{len(results['steps'])} steps passed"
    
    return results


@app.get("/search")
async def search_rfp(query: str, top_k: int = 5):
    """
    Search indexed RFP content using text query
    
    Args:
        query: Search query text
        top_k: Number of results to return
        
    Returns:
        dict: Search results
    """
    try:
        from document_processing.embedding import embed
        from document_processing.indexer import hybrid_search
        
        # Generate query embedding
        query_embedding = embed(query)
        
        # Perform hybrid search
        results = hybrid_search(query, query_embedding, top_k)
        
        return {
            "query": query,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/query")
async def query_rfp_semantic(question: str, top_k: int = 5, source: str = "mongo"):
    """
    Semantic search using natural language questions
    Example: /query?question=what is the business process?
    
    Args:
        question: Natural language question
        top_k: Number of results
        source: Data source - "mongo" or "search" (Azure)
        
    Returns:
        dict: Semantic search results
    """
    try:
        from search_rfp import query_rfp
        from document_processing.embedding import generate_embedding
        
        if source == "mongo":
            # Use MongoDB vector search
            results = query_rfp(question, top_k=top_k)
        else:
            # Use Azure Cognitive Search
            from document_processing.indexer import search_similar_chunks
            query_embedding = generate_embedding(question)
            results = search_similar_chunks(query_embedding, top_k=top_k)
        
        return {
            "question": question,
            "source": source,
            "results_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/analyze/{filename}")
async def analyze_rfp(filename: str):
    """
    Run all agents to analyze an RFP document
    
    Args:
        filename: Name of the file in blob storage
        
    Returns:
        dict: Comprehensive analysis from all agents
    """
    try:
        # Extract text from blob
        text = extract_text_from_blob(filename)
        
        # Run comprehensive analysis
        from agents.persona_agent import ComprehensiveAnalyzer
        analyzer = ComprehensiveAnalyzer()
        analysis = analyzer.analyze_all(text)
        
        return {
            "status": "success",
            "filename": filename,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
