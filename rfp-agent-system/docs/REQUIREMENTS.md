# RFP Process Enhancer - System Requirements

Complete list of all services, downloads, and dependencies required.

---

## ☁️ Azure Services Used

### 1. Azure Document Intelligence (Form Recognizer)
**Purpose**: PDF text extraction and OCR  
**Status**: ✅ Required  
**Why**: Extracts text from PDF documents with high accuracy  
**Credentials Needed**:
- Endpoint URL
- API Key

**Setup**:
1. Create resource in Azure Portal
2. Go to "Networking" → Enable "All networks" or add your IP
3. Copy endpoint and key from "Keys and Endpoint"

**Cost**: Pay-per-use (varies by pages processed)

---

### 2. Azure Blob Storage
**Purpose**: Document storage (optional)  
**Status**: ⚠️ Optional  
**Why**: Store and manage PDF documents in cloud  
**Credentials Needed**:
- Connection String
- Container Name

**Setup**:
1. Create Storage Account
2. Create container (e.g., "rfpenhancer1")
3. Copy connection string

**Cost**: Pay-per-GB storage + transactions

**Note**: You can process local PDFs without this service.

---

## 🖥️ Local Software Required

### 1. Ollama
**Purpose**: Local LLM for running 10 AI agents  
**Status**: ✅ Required  
**Download**: https://ollama.com/download  
**Model**: llama3 (4.7 GB)

**Installation**:
```bash
# 1. Download and install Ollama
# 2. Pull the model
ollama pull llama3

# 3. Verify
ollama list
```

**System Requirements**:
- RAM: 8 GB minimum (16 GB recommended)
- Disk: 5+ GB free space for model
- OS: Windows, macOS, or Linux

---

### 2. Python 3.9+
**Purpose**: Run the application  
**Status**: ✅ Required  
**Download**: https://www.python.org/downloads/

**Included in Project**:
- Already detected: Python 3.9.13

---

## 📦 Python Packages (Auto-Installed)

These are automatically installed from requirements or during setup:

### Core Dependencies
- **ollama** - LLM client
- **python-dotenv** - Environment configuration
- **azure-ai-formrecognizer** - Document Intelligence client
- **azure-storage-blob** - Blob storage operations
- **sentence-transformers** - Text embeddings
- **torch** - ML framework for embeddings
- **numpy** - Numerical operations
- **scikit-learn** - Vector similarity

### Already Installed (Confirmed)
✅ All packages verified in your environment

---

## 🔧 What Runs Where

### Cloud Services (Azure)
```
Your PDF → Azure Document Intelligence → Extracted Text
            ↓
         (Optional) Azure Blob Storage for document management
```

### Local Services (Your Machine)
```
Extracted Text → Chunking → Embeddings → Vector Store (JSON)
                                          ↓
                                    Ollama (llama3)
                                          ↓
                                    10 AI Agents
                                          ↓
                                    kb.md (Output)
```

---

## 💰 Cost Breakdown

### Azure Costs
| Service | Cost | Usage |
|---------|------|-------|
| Document Intelligence | ~$1.50 per 1000 pages | Per document processed |
| Blob Storage | ~$0.02 per GB/month | If using blob storage |

### Local Costs
| Service | Cost |
|---------|------|
| Ollama (llama3) | **FREE** |
| Python packages | **FREE** |
| Electricity | Minimal |

**Estimated**: ~$1-2 per 1000 pages processed

---

## 📋 Complete Setup Checklist

### Azure Setup
- [ ] Create Azure Document Intelligence resource
- [ ] Enable network access (All networks or your IP)
- [ ] Copy endpoint and key
- [ ] (Optional) Create Blob Storage account
- [ ] (Optional) Create container and copy connection string

### Local Setup
- [ ] Install Python 3.9+
- [ ] Install Ollama
- [ ] Pull llama3 model (`ollama pull llama3`)
- [ ] Configure `.env` file with Azure credentials
- [ ] Run `python backend/verify_setup.py`

### Verification
- [ ] Ollama running: `ollama list` shows llama3
- [ ] Python packages installed
- [ ] Azure credentials configured
- [ ] Process test document successfully

---

## 🔐 Required Credentials

Add these to `backend/.env`:

```env
# Required - Azure Document Intelligence
FORM_RECOGNIZER_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
FORM_RECOGNIZER_KEY=your_key_here

# Optional - Azure Blob Storage (if storing docs in cloud)
BLOB_CONN_STRING=DefaultEndpointsProtocol=https;AccountName=...
BLOB_CONTAINER_NAME=rfpenhancer1
```

---

## 🚫 What We DON'T Use

These are **NOT** required:
- ❌ Azure OpenAI (using local Ollama instead)
- ❌ Azure Cognitive Search (using local vector store)
- ❌ MongoDB (using JSON files)
- ❌ Any database (completely file-based)
- ❌ Docker (runs directly with Python)

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR MACHINE                          │
│                                                          │
│  ┌──────────────┐         ┌─────────────────┐          │
│  │   PDF File   │────────▶│  Python Script  │          │
│  └──────────────┘         └─────────────────┘          │
│                                    │                     │
│                                    ▼                     │
│                         ┌──────────────────┐            │
│                         │  Azure Document  │ (Cloud)    │
│                         │  Intelligence    │            │
│                         └──────────────────┘            │
│                                    │                     │
│                                    ▼                     │
│                         ┌──────────────────┐            │
│                         │  Text Chunking   │            │
│                         └──────────────────┘            │
│                                    │                     │
│                                    ▼                     │
│                         ┌──────────────────┐            │
│                         │   Embeddings     │            │
│                         │ (sentence-trans) │            │
│                         └──────────────────┘            │
│                                    │                     │
│                                    ▼                     │
│                         ┌──────────────────┐            │
│                         │  Local Vector    │            │
│                         │  Store (JSON)    │            │
│                         └──────────────────┘            │
│                                    │                     │
│                                    ▼                     │
│                         ┌──────────────────┐            │
│                         │   Ollama LLM     │            │
│                         │   (llama3)       │            │
│                         └──────────────────┘            │
│                                    │                     │
│                                    ▼                     │
│                         ┌──────────────────┐            │
│                         │   10 AI Agents   │            │
│                         └──────────────────┘            │
│                                    │                     │
│                                    ▼                     │
│                         ┌──────────────────┐            │
│                         │    kb.md         │            │
│                         │   (Output)       │            │
│                         └──────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Summary

### Cloud Services (2)
1. **Azure Document Intelligence** - Required for PDF extraction
2. **Azure Blob Storage** - Optional for document storage

### Local Software (2)
1. **Ollama with llama3** - Required for AI agents
2. **Python 3.9+** - Required to run application

### Total Setup Time
- First time: ~15-20 minutes
- Model download: ~5 minutes (one-time)
- Per document processing: 5-15 minutes

### Total Cost
- Setup: Free (except Azure account)
- Per document: ~$0.001-0.002 per page
- Monthly: Pay-as-you-go (no fixed costs)

---

**Everything is configured and ready to use!** ✅
