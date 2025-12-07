# 🚀 Complete Setup Checklist

## Current Status

✅ **Python 3.9.13** - Installed and configured  
✅ **All Python packages** - Installed (FastAPI, Azure SDKs, sentence-transformers, etc.)  
✅ **Azure credentials** - Configured in `.env`  
✅ **Code files** - All 10 agents, orchestrator, pipeline ready  
❌ **Ollama** - NOT RUNNING (needs to be installed/started)  

---

## 🔴 REQUIRED: Install and Start Ollama

### Step 1: Download Ollama

1. Go to: **https://ollama.com/download**
2. Download the Windows installer
3. Run the installer (it's quick, ~500MB)

### Step 2: Start Ollama Service

After installation, Ollama should auto-start. If not:

```cmd
# Check if running
ollama list

# If error, start Ollama by opening the Ollama app from Start Menu
# Or run:
ollama serve
```

### Step 3: Download the llama3 Model

```cmd
ollama pull llama3
```

This downloads the model (~4.7GB). Takes 5-10 minutes depending on internet speed.

### Step 4: Test Ollama

```cmd
ollama run llama3 "Hello, are you working?"
```

You should see a response from the AI.

---

## ✅ Everything Else is Ready!

### Your Current Configuration

| Component | Status | Notes |
|-----------|--------|-------|
| Python 3.9.13 | ✅ Working | All packages installed |
| Azure Blob Storage | ✅ Configured | Connection string in `.env` |
| Azure Document Intelligence | ✅ Configured | Endpoint and key in `.env` |
| Local Vector Store | ✅ Ready | No database needed |
| All 10 AI Agents | ✅ Created | Business Process, Gap, Persona, etc. |
| Pipeline | ✅ Ready | Processes docs end-to-end |
| Ollama LLM | ❌ Need to install | Download from ollama.com |

---

## 🎯 Once Ollama is Running

### Upload Your RFP Document to Azure

**Option 1: Using Azure Portal**
1. Go to https://portal.azure.com
2. Navigate to Storage Account `rfpenhancer1`
3. Click "Containers" → `rfpenhancer1`
4. Click "Upload" button
5. Select your RFP PDF/DOCX file
6. Click "Upload"

**Option 2: Using Command Line**
```cmd
cd "C:\Users\Karthik.Amaresh\Desktop\Hackathon 2025\RFP-Process-Enhancer\rfp-agent-system\backend"

& "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" blob_manager.py upload --file "C:\path\to\your\rfp-document.pdf"
```

### Process the Document

```cmd
cd "C:\Users\Karthik.Amaresh\Desktop\Hackathon 2025\RFP-Process-Enhancer\rfp-agent-system\backend"

& "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" pipeline.py --blob your-rfp-document.pdf
```

**That's it!** The system will:
1. ✅ Download from Azure Blob Storage
2. ✅ Extract text using Document Intelligence
3. ✅ Split into chunks
4. ✅ Generate embeddings locally
5. ✅ Store in local vector store (no database needed)
6. ✅ Run all 10 agents with Ollama
7. ✅ Save results to `kb.md`

---

## 📝 What the System Does

```
Your RFP Document (PDF/DOCX)
    ↓
Azure Blob Storage (private container)
    ↓
Azure Document Intelligence (OCR + text extraction)
    ↓
Text Chunking (500 words per chunk)
    ↓
Embedding Generation (sentence-transformers, locally)
    ↓
Local Vector Store (JSON file, no database)
    ↓
10 AI Agents analyze with Ollama llama3:
    • Business Process Agent
    • Gap Analysis Agent
    • Persona Agent
    • Pain Points Agent
    • Impact Assessment Agent
    • Challenges Agent
    • NFR (Non-Functional Requirements) Agent
    • Solution Architect Agent
    • Constraints Agent
    • Assumptions Agent
    ↓
Knowledge Base (kb.md) - All insights compiled
```

---

## 🔧 Quick Commands Reference

### List files in Azure
```cmd
& "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" blob_manager.py list
```

### Upload a file
```cmd
& "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" blob_manager.py upload --file "path\to\file.pdf"
```

### Process from Azure Blob
```cmd
& "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" pipeline.py --blob filename.pdf
```

### Process from local file (without Azure)
```cmd
& "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" pipeline.py --file "C:\path\to\local\file.pdf"
```

---

## ⚠️ Troubleshooting

### "Failed to connect to Ollama"
**Solution**: Make sure Ollama is installed and running
```cmd
ollama serve
```
Then try again.

### "Model 'llama3' not found"
**Solution**: Download the model
```cmd
ollama pull llama3
```

### "Blob not found"
**Solution**: Check blob name exactly
```cmd
& "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" blob_manager.py list
```
Copy the exact filename from the list.

### "Authentication failed"
**Solution**: Check `.env` file has complete connection string (one long line, no line breaks)

---

## 📊 Expected Processing Time

| Document Size | Processing Time |
|---------------|----------------|
| 10 pages | ~2-3 minutes |
| 50 pages | ~5-10 minutes |
| 100+ pages | ~15-20 minutes |

Time depends on:
- Document complexity
- Number of chunks generated
- Ollama model speed (llama3 is fast)

---

## 🎉 Summary

**You only need to:**

1. **Install Ollama** (one-time setup)
   - Download from https://ollama.com/download
   - Run installer
   - Pull llama3 model: `ollama pull llama3`

2. **Upload your RFP document** (per document)
   - Via Azure Portal, or
   - Via `blob_manager.py upload` command

3. **Run the pipeline** (per document)
   ```cmd
   & "C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python39_64/python.exe" pipeline.py --blob your-file.pdf
   ```

4. **Get results** (automatic)
   - Check `kb.md` for all insights
   - Check `data/embeddings/index.json` for searchable chunks

**That's all!** Everything else is already configured. 🚀
