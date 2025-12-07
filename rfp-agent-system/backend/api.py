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
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "RFP Process Enhancer API is running"}

@app.post("/api/process")
async def process_document(file: UploadFile = File(...)):
    """
    Process uploaded RFP document through the AI pipeline
    
    Args:
        file: PDF file uploaded by user
        
    Returns:
        JSON with processing results and generated knowledge base
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    # Create temporary file to save upload
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
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
            "output": kb_content
        })
        
    except Exception as e:
        import traceback
        error_detail = f"Processing failed: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
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

if __name__ == "__main__":
    import uvicorn
    print("Starting RFP Process Enhancer API server...")
    print("API documentation available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
