# Pipeline Validation Guide

## Quick Validation Steps

### 1. Check API Health
```bash
curl http://localhost:8000/health
```

### 2. Validate Pipeline Components
```bash
curl -X POST http://localhost:8000/validate-pipeline
```

### 3. Test Upload & Processing
```bash
curl -X POST -F "file=@your_rfp.pdf" http://localhost:8000/upload
```

### 4. Search Indexed Content
```bash
curl "http://localhost:8000/search?query=your+search+term&top_k=5"
```

### 5. Analyze RFP Document
```bash
curl -X POST http://localhost:8000/analyze/your_rfp.pdf
```

## API Endpoints

### Core Endpoints
- `GET /` - API status
- `GET /health` - Health check for all services
- `POST /validate-pipeline` - Validate pipeline components

### Document Processing
- `POST /upload` - Upload and process RFP (complete pipeline)
- `POST /extract-text/{filename}` - Extract text only
- `POST /extract-structured/{filename}` - Extract with structure

### Search & Analysis
- `GET /search?query={text}&top_k={number}` - Search indexed documents
- `POST /analyze/{filename}` - Run all agents analysis

## Validation Checklist

### Before Running
- [ ] Create `.env` file with Azure credentials
- [ ] Install all dependencies
- [ ] Ensure Azure services are provisioned

### Testing Steps
1. **Start Server**
   ```bash
   python backend/main.py
   ```

2. **Check Health**
   - Visit: http://localhost:8000/health
   - Verify all services show "connected" or "configured"

3. **Validate Pipeline**
   - Visit: http://localhost:8000/validate-pipeline
   - All 4 steps should show "success"

4. **Test Upload**
   - Upload a test PDF
   - Check response for chunk count
   - Verify file appears in blob storage

5. **Test Search**
   - Search for content from uploaded file
   - Verify results are returned

6. **Test Analysis**
   - Run analysis on uploaded file
   - Verify all 6 agents return results

## Expected Results

### Health Check Response
```json
{
  "api": "healthy",
  "services": {
    "blob_storage": "connected",
    "form_recognizer": "configured",
    "azure_openai": "configured",
    "azure_search": "configured",
    "embedding_model": {
      "model_name": "all-MiniLM-L6-v2",
      "embedding_dimension": 384,
      "max_seq_length": 256
    }
  }
}
```

### Pipeline Validation Response
```json
{
  "pipeline": "validation",
  "overall_status": "success",
  "summary": "4/4 steps passed",
  "steps": [
    {"step": "1. Text Chunking", "status": "success"},
    {"step": "2. Embedding Generation", "status": "success"},
    {"step": "3. Search Index Connection", "status": "success"},
    {"step": "4. Blob Storage Connection", "status": "success"}
  ]
}
```

### Upload Response
```json
{
  "status": "indexed",
  "filename": "your_rfp.pdf",
  "chunks": 25,
  "text_length": 15000
}
```

## Troubleshooting

### Common Issues

1. **Service Not Configured**
   - Check `.env` file has all required keys
   - Verify Azure credentials are valid

2. **Connection Errors**
   - Ensure Azure services are running
   - Check firewall/network settings
   - Verify connection strings

3. **Model Loading Failed**
   - First run downloads model (may take time)
   - Check internet connection
   - Verify disk space

4. **Index Not Found**
   - Run index creation script first
   - Check index name matches config

## Manual Testing with Python

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Validate pipeline
response = requests.post("http://localhost:8000/validate-pipeline")
print(response.json())

# Upload file
with open("test_rfp.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/upload",
        files={"file": f}
    )
print(response.json())

# Search
response = requests.get(
    "http://localhost:8000/search",
    params={"query": "business process", "top_k": 5}
)
print(response.json())
```

## Performance Benchmarks

### Expected Processing Times
- Upload (10 MB PDF): ~5-10 seconds
- Text Extraction: ~3-5 seconds
- Chunking: <1 second
- Embedding (100 chunks): ~2-3 seconds
- Indexing (100 chunks): ~2-3 seconds
- Search query: <1 second
- Agent analysis: ~10-15 seconds (all 6 agents)

## Next Steps

1. Create search index (first time only)
2. Test with sample RFP documents
3. Verify agent analysis quality
4. Test search relevance
5. Monitor performance metrics
