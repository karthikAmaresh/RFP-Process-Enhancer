# RFP Process Enhancer - Setup Guide

Complete setup instructions for the RFP Analysis System with 10 AI agents.

---

## 📋 Prerequisites

- **Python 3.9+**
- **Ollama** with llama3 model
- **Azure Account** (for Document Intelligence)

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Install Ollama

1. Download from: https://ollama.com/download
2. Install the application
3. Pull the llama3 model:
   ```bash
   ollama pull llama3
   ```
4. Verify installation:
   ```bash
   ollama list
   ```

### Step 2: Configure Azure Document Intelligence

1. Go to Azure Portal: https://portal.azure.com
2. Create/Navigate to your Document Intelligence resource
3. Go to **"Networking"** → Enable **"All networks"** or add your IP
4. Copy credentials from **"Keys and Endpoint"**

### Step 3: Configure Environment Variables

Edit `backend/.env` file:

```env
# Azure Blob Storage (optional - for document storage)
BLOB_CONN_STRING=your_connection_string_here
BLOB_CONTAINER_NAME=rfpenhancer1

# Azure Document Intelligence (required - for PDF extraction)
FORM_RECOGNIZER_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
FORM_RECOGNIZER_KEY=your_key_here
```

### Step 4: Verify Setup

```bash
cd backend
python verify_setup.py
```

This checks:
- Python packages installed
- Ollama running with llama3
- Azure credentials configured

### Step 5: Process Your First Document

```bash
cd rfp-agent-system
python backend/pipeline.py --file "your-document.pdf"
```

Results saved to: `backend/kb.md`

---

## 📁 Project Structure

```
rfp-agent-system/
├── backend/
│   ├── agents/              # 10 AI agents
│   ├── prompts/             # Agent prompts
│   ├── document_processing/ # PDF extraction
│   ├── pipeline.py          # Main script
│   ├── config.py            # Configuration
│   └── .env                 # Credentials
├── docs/                    # Documentation
└── kb.md                    # Generated output
```

---

## 🎯 Usage

### Process Local PDF
```bash
python backend/pipeline.py --file "document.pdf"
```

### Process from Azure Blob
```bash
python backend/pipeline.py --blob "document.pdf"
```

### View Results
Open `backend/kb.md` to see analysis from all 10 agents.

---

## 🔧 Configuration Details

### Azure Document Intelligence

**Required for**: PDF text extraction and OCR

**Setup**:
1. Create resource in Azure Portal
2. Enable network access (Networking → All networks)
3. Copy endpoint and key to `.env`

### Azure Blob Storage

**Required for**: Optional document storage

**Setup**:
1. Create Storage Account in Azure Portal
2. Create container (e.g., "rfpenhancer1")
3. Copy connection string to `.env`

**Note**: If blob has disabled public access, connection string authentication still works.

### Ollama LLM

**Required for**: Running all 10 AI agents

**Models**:
- Default: `llama3` (4.7 GB)
- Alternatives: `llama2`, `mistral`, `mixtral`

**Change model** in `backend/llm_client.py`:
```python
def local_llm(prompt: str, model: str = "llama3"):
```

---

## 🤖 The 10 AI Agents

1. **Business Process** - Current workflows
2. **Gap Analysis** - Improvement areas
3. **Personas** - User types and stakeholders
4. **Pain Points** - Problems to solve
5. **Impact** - Budget, scale, deadlines
6. **Challenges** - Technical issues
7. **NFR** - Non-functional requirements
8. **Architect** - Technical design
9. **Constraints** - Limitations
10. **Assumptions** - Dependencies

---

## 📊 Processing Pipeline

```
PDF Document
    ↓
[1/5] Text Extraction (Azure Document Intelligence)
    ↓
[2/5] Text Chunking (500 words/chunk)
    ↓
[3/5] Generate Embeddings (sentence-transformers)
    ↓
[4/5] Run 10 AI Agents (Ollama llama3)
    ↓
[5/5] Save to Knowledge Base (kb.md)
```

**Expected time**: 5-15 minutes per document

---

## 🐛 Troubleshooting

### "Model 'llama3' not found"
**Solution**: Pull the model
```bash
ollama pull llama3
```

### "(403) Public access is disabled"
**Solution**: Enable network access on Document Intelligence
1. Azure Portal → Your Document Intelligence resource
2. Networking → Allow "All networks"
3. Save and wait 1-2 minutes

### "Failed to connect to Ollama"
**Solution**: Start Ollama service
- Windows: Open Ollama app from Start Menu
- Mac/Linux: `ollama serve`

### "Azure credentials not configured"
**Solution**: Check `.env` file has complete credentials
- No line breaks in connection strings
- No extra spaces before/after `=`

---

## 📈 Performance Tips

1. **Large Documents**: Split into smaller files for faster processing
2. **Multiple Documents**: Process sequentially (agents use same LLM)
3. **Faster LLM**: Use smaller models like `llama2` or `mistral`
4. **Network Issues**: Process local PDFs instead of from blob storage

---

## 🔐 Security Best Practices

1. ✅ Keep `.env` file private (never commit to git)
2. ✅ Use `.gitignore` to exclude `.env`
3. ✅ Rotate Azure keys periodically
4. ✅ Use private blob storage containers
5. ✅ Restrict Document Intelligence network access to your IP

---

## 📞 Support

- **Check Logs**: Terminal output shows detailed progress
- **Verify Setup**: Run `python verify_setup.py`
- **Review Docs**: See other files in `docs/` folder

---

## ✅ Quick Checklist

- [ ] Ollama installed with llama3 model
- [ ] Azure Document Intelligence credentials in `.env`
- [ ] Network access enabled on Document Intelligence
- [ ] Python 3.9+ installed
- [ ] Run `verify_setup.py` successfully
- [ ] Processed first document successfully

---

**Ready to analyze RFPs!** 🚀
