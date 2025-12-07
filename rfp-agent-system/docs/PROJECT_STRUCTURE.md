# Project Structure

```
rfp-agent-system/
└── backend/
    ├── agents/                      # AI Agent modules
    │   ├── __init__.py
    │   ├── base_agent.py           # Abstract base class
    │   ├── business_process_agent.py
    │   ├── gap_agent.py
    │   ├── persona_agent.py
    │   ├── pain_point_agent.py
    │   ├── impact_agent.py
    │   ├── challenge_agent.py
    │   ├── nfr_agent.py
    │   ├── architect_agent.py
    │   ├── constraints_agent.py
    │   └── assumptions_agent.py
    │
    ├── prompts/                     # Agent prompt templates
    │   ├── business_process.txt
    │   ├── gap.txt
    │   ├── persona.txt
    │   ├── pain_points.txt
    │   ├── impact.txt
    │   ├── challenges.txt
    │   ├── nfr.txt
    │   ├── architect.txt
    │   ├── constraints.txt
    │   └── assumptions.txt
    │
    ├── document_processing/         # Document handling
    │   ├── __init__.py
    │   ├── extract_text.py         # Azure Document Intelligence
    │   ├── chunking.py             # Text chunking
    │   └── embedding.py            # Embedding generation
    │
    ├── embedding/                   # Embedding utilities
    │   ├── __init__.py
    │   └── embedder.py             # sentence-transformers
    │
    ├── memory/                      # Short-term memory
    │   ├── __init__.py
    │   └── short_term_memory.py    # Simple dict storage
    │
    ├── data/                        # Generated data
    │   ├── chunks/                 # Text chunks
    │   ├── embeddings/             # Vector embeddings
    │   │   └── index.json          # Local vector store
    │   └── raw_text/               # Extracted text
    │
    ├── config.py                    # Configuration settings
    ├── llm_client.py               # Ollama LLM interface
    ├── orchestrator.py             # Agent orchestration
    ├── pipeline.py                 # Main processing pipeline
    ├── local_vector_store.py       # Local vector storage
    ├── blob_manager.py             # Azure Blob operations
    ├── verify_setup.py             # System verification
    │
    ├── .env                        # Environment variables (private)
    ├── .env.example                # Template for .env
    │
    ├── README.md                   # Project documentation
    ├── QUICKSTART_GUIDE.md         # Quick start guide
    ├── SETUP_CHECKLIST.md          # Setup instructions
    ├── ARCHITECTURE.md             # Architecture details
    ├── AZURE_CREDENTIALS_GUIDE.md  # Azure setup help
    ├── PRIVATE_BLOB_GUIDE.md       # Private blob guide
    │
    └── kb.md                       # Generated knowledge base (output)
```

## File Descriptions

### Core Files
- **`pipeline.py`**: Main entry point for processing RFP documents
- **`orchestrator.py`**: Coordinates all 10 agents and manages workflow
- **`llm_client.py`**: Interface to Ollama LLM (llama3)
- **`config.py`**: Configuration and environment variables
- **`local_vector_store.py`**: JSON-based vector storage

### Agents
- Each agent inherits from `base_agent.py`
- Analyzes specific aspect of RFP
- Uses prompt template from `prompts/`

### Document Processing
- **`extract_text.py`**: PDF → Text (Azure Document Intelligence)
- **`chunking.py`**: Split text into manageable chunks
- **`embedding.py`**: Generate vector embeddings

### Utilities
- **`blob_manager.py`**: Upload/download from Azure Blob
- **`verify_setup.py`**: Check system configuration

### Documentation
- **`README.md`**: Main documentation
- **`QUICKSTART_GUIDE.md`**: Getting started
- **`SETUP_CHECKLIST.md`**: Setup steps
- **`ARCHITECTURE.md`**: Technical architecture
- **`AZURE_CREDENTIALS_GUIDE.md`**: Azure setup
- **`PRIVATE_BLOB_GUIDE.md`**: Private blob access

### Output
- **`kb.md`**: Generated knowledge base with all agent analyses
- **`data/chunks/`**: Text chunks from documents
- **`data/embeddings/index.json`**: Local vector store

## Technology Stack

- **Python 3.9+**
- **Ollama** (llama3) - Local LLM
- **Azure Document Intelligence** - PDF extraction
- **Azure Blob Storage** - Document storage
- **sentence-transformers** - Embeddings
- **FastAPI** - (optional) API framework

## Clean Architecture Principles

1. **Separation of Concerns**: Each agent handles one analysis type
2. **Dependency Injection**: LLM and prompts injected into agents
3. **Abstract Base Class**: Common interface for all agents
4. **Local-First**: No mandatory cloud dependencies (except PDF extraction)
5. **Modular Design**: Easy to add/remove agents
