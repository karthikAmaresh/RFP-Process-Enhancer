# RFP Process Enhancer - Updated Architecture

## Overview
This system processes RFP documents using Azure services for document handling and local LLMs (Ollama) for analysis.

## Architecture Components

### Azure Services (Used)
1. **Azure Blob Storage** - Document storage
2. **Azure Document Intelligence** - PDF text extraction and OCR

### Local Services (Used)
1. **Ollama (llama3)** - Local LLM for all agent analysis
2. **Sentence Transformers** - Local embedding generation (all-mpnet-base-v2)

### Azure Services (NOT Used)
- ~~Azure AI Search~~ - Replaced with local processing
- ~~Azure OpenAI~~ - Replaced with Ollama

## System Flow

```
Documents → Blob Storage → Document Intelligence → Text Extraction
                                                          ↓
                                                      Chunking
                                                          ↓
                                                  Embedding (Local)
                                                          ↓
                                              Agent Analysis (Ollama)
                                                          ↓
                                              Short-term Memory Store
                                                          ↓
                                                  Knowledge Base (kb.md)
```

## AI Agents (10 Total)

1. **BusinessProcessAgent** - Extract current business processes
2. **GapAgent** - Identify gaps between current and proposed
3. **PersonaAgent** - Identify users and their needs
4. **PainPointsAgent** - Extract problems that need solving
5. **ImpactfulStatementsAgent** - Budget, scale, compliance
6. **ChallengesAgent** - Technical and operational challenges
7. **NFRAgent** - Non-functional requirements
8. **ArchitectAgent** - Architecture requirements
9. **ConstraintsAgent** - Constraints and limitations
10. **AssumptionsAgent** - Assumptions and dependencies

## Setup Instructions

### 1. Install Ollama
```bash
# Install Ollama from https://ollama.ai
# Pull llama3 model
ollama pull llama3
```

### 2. Install Python Dependencies
```bash
pip install ollama sentence-transformers azure-storage-blob azure-ai-formrecognizer fastapi uvicorn
```

### 3. Configure Azure Services
Create `.env` file:
```env
# Azure Blob Storage (Required)
BLOB_CONN_STRING=your_connection_string
BLOB_CONTAINER_NAME=rfp-documents

# Azure Document Intelligence (Required for PDFs)
FORM_RECOGNIZER_ENDPOINT=your_endpoint
FORM_RECOGNIZER_KEY=your_key

# MongoDB (Optional - for vector storage)
MONGO_CONN_STR=

# Azure OpenAI (NOT USED - using Ollama instead)
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_DEPLOYMENT=

# Azure AI Search (NOT USED - local processing)
SEARCH_ENDPOINT=
SEARCH_API_KEY=
SEARCH_INDEX_NAME=
```

## Usage

### Option 1: Process from Blob Storage
```bash
python pipeline.py --blob my-rfp-document.pdf
```

### Option 2: Process Local File
```bash
python pipeline.py --file path/to/rfp.txt
```

### Option 3: Use Orchestrator Directly
```python
from orchestrator import run_all_agents, save_to_kb

text = "Your RFP content here..."
results = run_all_agents(text)
save_to_kb(results)
```

### Option 4: Test Individual Agents
```python
from agents.business_process_agent import BusinessProcessAgent
from llm_client import local_llm

llm = local_llm
agent = BusinessProcessAgent(llm, open("prompts/business_process.txt").read())
output = agent.extract("Your RFP text here")
print(output)
```

## Project Structure

```
backend/
├── agents/
│   ├── base_agent.py              # Base class for all agents
│   ├── business_process_agent.py
│   ├── gap_agent.py
│   ├── persona_agent.py
│   ├── pain_point_agent.py
│   ├── impact_agent.py
│   ├── challenge_agent.py
│   ├── nfr_agent.py              # New: Non-functional requirements
│   ├── architect_agent.py         # New: Architecture requirements
│   ├── constraints_agent.py       # New: Constraints
│   └── assumptions_agent.py       # New: Assumptions & dependencies
├── prompts/
│   ├── business_process.txt
│   ├── gap.txt
│   ├── persona.txt
│   ├── pain_points.txt
│   ├── impact.txt
│   ├── challenges.txt
│   ├── nfr.txt                    # New
│   ├── architect.txt              # New
│   ├── constraints.txt            # New
│   └── assumptions.txt            # New
├── document_processing/
│   ├── extract_text.py           # Azure Document Intelligence
│   ├── chunking.py               # Text chunking
│   └── indexer.py                # (Optional) Azure Search integration
├── embedding/
│   └── embedder.py               # Local embedding generation
├── memory/
│   └── short_term_memory.py      # Simple in-memory storage
├── data/
│   ├── chunks/                   # Generated text chunks
│   └── raw_text/                 # Raw extracted text
├── llm_client.py                 # Ollama integration
├── orchestrator.py               # Main agent orchestration
├── pipeline.py                   # Complete processing pipeline
├── config.py                     # Configuration management
└── main.py                       # FastAPI server (optional)
```

## Output

The system generates a `kb.md` (Knowledge Base) file with all agent outputs:

```markdown
## BUSINESS_PROCESS
- Current system capabilities...
- Key workflows...

## GAP
- Missing features...
- Improvement areas...

## PERSONAS
- User roles...
- User needs...

... (all other agents)
```

## API Endpoints (if using FastAPI)

- `POST /upload` - Upload and process document
- `POST /analyze` - Analyze text with all agents
- `GET /health` - Health check
- `GET /agents` - List all available agents

## Performance Notes

- **Ollama (local)**: ~5-10 seconds per agent on CPU
- **Azure Document Intelligence**: ~2-5 seconds per page
- **Embedding generation**: ~100ms per chunk
- **Total processing time**: ~2-3 minutes for typical RFP document

## Advantages of This Architecture

✅ **Cost-effective**: No Azure OpenAI charges, only Document Intelligence  
✅ **Privacy**: LLM processing happens locally  
✅ **Flexible**: Easy to switch LLM models  
✅ **Fast**: Local LLM inference with Ollama  
✅ **Scalable**: Can process multiple documents in parallel  

## Next Steps

1. Test with your RFP documents
2. Tune prompts for better extraction
3. Add more specialized agents as needed
4. Implement caching for repeated analysis
5. Add vector search with FAISS or ChromaDB locally
