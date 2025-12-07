# RFP Process Enhancer

AI-powered RFP document analysis system with 10 specialized agents.

## 🎯 Features

- **10 Specialized AI Agents** - Analyzes different aspects of RFPs
- **Local LLM** - Uses Ollama (llama3) - no cloud AI costs
- **Azure Document Intelligence** - PDF extraction and OCR
- **Local Vector Storage** - No database required
- **Knowledge Base Generation** - Comprehensive analysis in markdown

## 🚀 Quick Start

```bash
# 1. Install Ollama and pull model
ollama pull llama3

# 2. Configure Azure credentials in backend/.env
# FORM_RECOGNIZER_ENDPOINT=...
# FORM_RECOGNIZER_KEY=...

# 3. Process a document
python backend/pipeline.py --file "document.pdf"

# 4. View results in backend/kb.md
```

## 📊 The 10 AI Agents

| Agent | Purpose |
|-------|---------|
| Business Process | Current workflows and activities |
| Gap Analysis | Improvement areas |
| Personas | User types and stakeholders |
| Pain Points | Problems to solve |
| Impact | Budget, scale, deadlines |
| Challenges | Technical issues |
| NFR | Non-functional requirements |
| Architect | Technical design |
| Constraints | Limitations |
| Assumptions | Dependencies |

## 📁 Project Structure

```
backend/
├── agents/              # 10 AI agents
├── prompts/             # Agent prompt templates
├── document_processing/ # PDF extraction & chunking
├── pipeline.py          # Main processing script
├── orchestrator.py      # Agent coordination
├── llm_client.py        # Ollama interface
└── config.py            # Configuration
```

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Complete installation instructions
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Detailed architecture
- **[Architecture](docs/ARCHITECTURE.md)** - Technical design

## 🔧 Requirements

- Python 3.9+
- Ollama with llama3 model
- Azure Document Intelligence

## 📈 Processing Pipeline

```
PDF → Text Extraction → Chunking → Embeddings → 10 AI Agents → kb.md
```

**Expected time**: 5-15 minutes per document

---

**Built with**: Python • Ollama • Azure AI • sentence-transformers
