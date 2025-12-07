# Quick Start Guide - RFP Process Enhancer

## Step 1: Get Your Azure Credentials

### A. Document Intelligence (Form Recognizer)

1. Go to [Azure Portal](https://portal.azure.com)
2. Find your **Document Intelligence** resource
3. Click **"Keys and Endpoint"** in left menu
4. Copy:
   - **Endpoint** (e.g., `https://your-resource.cognitiveservices.azure.com/`)
   - **Key 1** (long string of characters)

### B. Blob Storage

1. Go to your **Storage Account** in Azure Portal
2. Click **"Access keys"** in left menu
3. Click **"Show"** next to key1
4. Copy the **Connection string** (starts with `DefaultEndpointsProtocol=https...`)
5. Note your **container name** (you created it, e.g., `rfp-documents`)

## Step 2: Update Your .env File

Open the `.env` file and paste your credentials:

```env
# Azure Document Intelligence
FORM_RECOGNIZER_ENDPOINT=https://YOUR-RESOURCE.cognitiveservices.azure.com/
FORM_RECOGNIZER_KEY=your_key_here

# Azure Blob Storage
BLOB_CONN_STRING=DefaultEndpointsProtocol=https;AccountName=yourname;AccountKey=yourkey;EndpointSuffix=core.windows.net
BLOB_CONTAINER_NAME=rfp-documents

# Leave these empty (not needed for local LLM)
MONGO_CONN_STR=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=
SEARCH_ENDPOINT=
SEARCH_API_KEY=
SEARCH_INDEX_NAME=
```

## Step 3: Install Ollama

### Windows:
1. Download from https://ollama.ai
2. Run installer
3. Open Command Prompt and run:
   ```cmd
   ollama pull llama3
   ```

### Verify Ollama is running:
```cmd
ollama list
```
You should see `llama3` in the list.

## Step 4: Install Python Dependencies

```cmd
cd "C:\Users\Karthik.Amaresh\Desktop\Hackathon 2025\RFP-Process-Enhancer\rfp-agent-system\backend"
pip install ollama sentence-transformers azure-storage-blob azure-ai-formrecognizer
```

## Step 5: Upload a Test Document

### Option A: Upload to Azure Blob Storage
1. Go to your Storage Account in Azure Portal
2. Navigate to your container (`rfp-documents`)
3. Click **Upload**
4. Upload a sample RFP document (PDF or TXT)

### Option B: Use a Local File
Create a test file `sample_rfp.txt` with some RFP content.

## Step 6: Run the Pipeline

### From Blob Storage:
```cmd
python pipeline.py --blob your-document.pdf
```

### From Local File:
```cmd
python pipeline.py --file sample_rfp.txt
```

### Expected Output:
```
============================================================
RFP PROCESSING PIPELINE
============================================================

[1/5] Extracting text from document...
✓ Extracted text from blob: your-document.pdf
Document length: 12534 characters

[2/5] Chunking text...
✓ Created 8 chunks
✓ Saved chunks to data/chunks/

[3/5] Generating embeddings and storing locally...
  Processed 8/8 chunks
✓ Generated 8 embeddings (768-dim)
✓ Stored in local vector store: 8 chunks

[4/5] Running AI agents for analysis...
Running business_process agent...
Running gap agent...
Running personas agent...
Running pain_points agent...
Running impact agent...
Running challenges agent...
Running nfr agent...
Running architecture agent...
Running constraints agent...
Running assumptions agent...
✓ Completed analysis with 10 agents

[5/5] Saving results to knowledge base...
✓ Results saved to kb.md

============================================================
PROCESSING COMPLETE
============================================================
```

## Step 7: Check Your Results

1. **Knowledge Base**: Open `kb.md` to see all agent analysis
2. **Chunks**: Check `data/chunks/` folder for text chunks
3. **Vector Store**: Check `data/embeddings/index.json` for embeddings

## Testing Individual Components

### Test Ollama Connection:
```cmd
python llm_client.py
```

### Test Vector Store:
```cmd
python local_vector_store.py
```

### Test Single Agent:
```cmd
python test_agents.py
```

### Test Orchestrator:
```cmd
python orchestrator.py
```

## Troubleshooting

### "ollama not found" or "connection refused"
- Make sure Ollama is running: `ollama serve`
- Or restart Ollama app on Windows

### "Azure Document Intelligence error"
- Check your endpoint has `/` at the end
- Verify your key is correct
- Make sure your resource is active

### "Blob not found"
- Check container name matches in `.env`
- Verify blob name is correct (case-sensitive)
- Make sure you uploaded the file to Azure

### "Module not found"
- Run: `pip install -r requirements.txt`
- Or install missing package: `pip install <package-name>`

## What Works WITHOUT Vector Database

✅ **Everything works!** The system uses a simple JSON-based local vector store:
- Text extraction
- Chunking
- Embedding generation
- Agent analysis
- Similarity search
- Knowledge base creation

📝 **Stored in:** `data/embeddings/index.json`

## Next Steps

1. ✅ Upload your real RFP documents
2. ✅ Process them with the pipeline
3. ✅ Review the generated `kb.md`
4. ✅ Use the vector store to search similar content
5. ✅ Customize agent prompts in `prompts/` folder
6. ✅ Add more agents as needed

## Quick Reference Commands

```cmd
# Process from Azure Blob
python pipeline.py --blob my-rfp.pdf

# Process local file
python pipeline.py --file my-rfp.txt

# Run all agents on text
python orchestrator.py

# Test components
python test_agents.py
python local_vector_store.py

# Search similar chunks
python -c "from local_vector_store import LocalVectorStore; store = LocalVectorStore(); print(store.search_similar('what is the budget?'))"
```

## Need Help?

Check these files:
- `ARCHITECTURE.md` - System design
- `README.md` - Project overview
- `.env.example` - Configuration template
