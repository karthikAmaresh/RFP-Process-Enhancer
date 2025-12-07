# Quick Start Guide - Run Locally

## Prerequisites
✅ Python 3.9+ installed
✅ All packages installed (fastapi, uvicorn, sentence-transformers, pymongo, etc.)

## Step 1: Configure Environment

Create a `.env` file in the `backend` folder:

```bash
cd rfp-agent-system/backend
```

Create `.env` file (you can start with minimal config):
```env
# Minimal for local testing
MONGO_CONN_STR=mongodb://localhost:27017/
MONGO_DB_NAME=rfp_db

# Optional - Azure services (leave empty for testing without Azure)
AZURE_BLOB_CONNECTION_STRING=
BLOB_CONTAINER_NAME=rfp-documents
AZURE_FORM_RECOGNIZER_ENDPOINT=
AZURE_FORM_RECOGNIZER_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
SEARCH_INDEX_NAME=rfp-index
```

## Step 2: Install MongoDB (Optional for full testing)

### Option A: Docker (Recommended)
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Option B: MongoDB Community Edition
Download from: https://www.mongodb.com/try/download/community

### Option C: Skip MongoDB
You can test without MongoDB - just use Azure Search or local testing only

## Step 3: Start the Server

```bash
# Navigate to backend folder
cd rfp-agent-system/backend

# Run the server
python main.py
```

The server will start at: **http://localhost:8000**

## Step 4: Test in Browser

Open your browser and visit:

### 1. API Documentation
```
http://localhost:8000/docs
```
This shows interactive API documentation (Swagger UI)

### 2. Health Check
```
http://localhost:8000/health
```
Shows status of all services

### 3. Pipeline Validation
```
http://localhost:8000/validate-pipeline
```
Tests all components without uploading files

## Step 5: Test with Python Script

Run the test script:
```bash
cd rfp-agent-system
python test_pipeline.py
```

Or test with a file:
```bash
python test_pipeline.py path/to/your/test.pdf
```

## Step 6: Test Basic Functionality

### Test 1: Process Sample Text (No Azure needed)
```bash
# In backend folder
python -c "from process_rfp import process_rfp; print(process_rfp('This is a test RFP document with sample content.', filename='test.txt', storage='mongo'))"
```

### Test 2: Test Embedding Generation
```bash
python -c "from document_processing.embedding import generate_embedding; print(len(generate_embedding('test')))"
```
Should output: 768 (embedding dimension)

### Test 3: Test Chunking
```bash
python -c "from document_processing.chunking import chunk_text; chunks = chunk_text('word ' * 500); print(f'Created {len(chunks)} chunks')"
```

### Test 4: Search Query (after processing some data)
```bash
python -c "from search_rfp import query_rfp; print(query_rfp('what is the business process?'))"
```

## Testing with API Calls

### Using curl (Windows PowerShell):

1. **Health Check**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" | Select-Object -Expand Content
```

2. **Validate Pipeline**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/validate-pipeline" -Method POST | Select-Object -Expand Content
```

3. **Upload File** (if you have a test PDF)
```powershell
$file = [System.IO.File]::ReadAllBytes("test.pdf")
Invoke-WebRequest -Uri "http://localhost:8000/upload" -Method POST -InFile "test.pdf" -ContentType "multipart/form-data"
```

### Using Python requests:

Create `test_local.py`:
```python
import requests

BASE_URL = "http://localhost:8000"

# Test health
print("Testing health...")
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Test validation
print("\nTesting pipeline validation...")
response = requests.post(f"{BASE_URL}/validate-pipeline")
print(response.json())

print("\n✅ Server is running!")
```

Run:
```bash
python test_local.py
```

## Quick Test Without MongoDB

If you don't have MongoDB, you can still test:

1. Modify `storage` parameter to use `"search"` instead of `"mongo"`
2. Or just test components individually:

```python
# Test embedding
from document_processing.embedding import generate_embedding
vec = generate_embedding("test text")
print(f"Embedding dimension: {len(vec)}")

# Test chunking
from document_processing.chunking import chunk_text
chunks = chunk_text("This is a test. " * 100)
print(f"Chunks created: {len(chunks)}")
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Module Not Found
```bash
# Make sure you're in the right directory
cd rfp-agent-system/backend
# Or add to Python path
set PYTHONPATH=%CD%
```

### Model Download Taking Long
First run downloads the embedding model (~420MB). Be patient!

### MongoDB Connection Failed
- Check MongoDB is running: Task Manager or `docker ps`
- Or set `storage="search"` in process_rfp calls
- Or skip MongoDB-dependent tests

## What to Expect

### First Run:
- Downloads embedding model (all-mpnet-base-v2)
- Takes 1-2 minutes for first request
- Subsequent requests are fast

### Health Check Response:
```json
{
  "api": "healthy",
  "services": {
    "blob_storage": "error: ..." (OK if no Azure),
    "embedding_model": {
      "model_name": "all-mpnet-base-v2",
      "embedding_dimension": 768
    }
  }
}
```

### Pipeline Validation:
```json
{
  "overall_status": "success",
  "summary": "4/4 steps passed"
}
```

## Next Steps

1. ✅ Server running → Test with sample text
2. ✅ Processing works → Upload a real RFP
3. ✅ Search working → Test agent analysis
4. ✅ Everything local → Add Azure services

## Need Help?

- Check logs in terminal where server is running
- Visit `/docs` for interactive API testing
- Run `python test_pipeline.py` for automated checks
