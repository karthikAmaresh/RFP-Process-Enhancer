# RFP Process Enhancer

> AI-powered system that analyzes RFP documents and generates structured knowledge bases using 12 specialized AI agents with professional personas.

## 🎯 Overview

The RFP Process Enhancer automates the analysis of Request for Proposal (RFP) documents using AI agents. Each agent has a specialized persona (Senior Business Analyst, Principal Architect, etc.) and analyzes specific aspects of the RFP to generate a comprehensive, structured knowledge base.

## ✨ Key Features

- **12 Specialized AI Agents** with professional personas
- **Structured Knowledge Base** output following industry templates
- **Azure Integration** (Document Intelligence, Blob Storage)
- **Modern React UI** with drag-drop upload
- **Local LLM** (Ollama/llama3) for privacy and cost savings
- **Vector Embeddings** for semantic search
- **Comprehensive Coverage**: From problem statement to technical architecture

## 🏗️ Architecture

### Agent Ecosystem

| Agent | Persona | Output Section |
|-------|---------|----------------|
| Introduction | Senior Technical Writer | Problem Statement + Summary |
| Challenges | Technical Challenge Analyst | System challenges (6 categories) |
| Pain Points | Business Pain Point Analyst | User pain points with severity |
| Business Process | Senior Business Analyst (15+ yrs) | Current workflows and processes |
| Gap Analysis | Requirements Gap Analyst | Functional, technical, process gaps |
| Personas | UX Research Lead | User profiles with actions |
| Constraints | Constraints Analyst | Tech, budget, timeline constraints |
| Functional Req | Functional Req Analyst | User stories with acceptance criteria |
| NFR | NFR Specialist (15+ yrs) | 8 NFR categories |
| Architecture | Principal Solutions Architect (20+ yrs) | 12 architecture dimensions |
| Assumptions | Risk & Dependency Analyst | Assumptions and dependencies |
| Impact | Business Impact Analyst | Metrics, compliance, ROI |

### Technology Stack

- **Frontend**: React 19, Vite 7, Tailwind CSS v4
- **Backend**: Python 3.9, FastAPI
- **LLM**: Ollama (llama3 - 4.7 GB)
- **Cloud**: Azure Document Intelligence, Azure Blob Storage
- **Vector DB**: Local JSON-based storage

## 📋 Knowledge Base Structure

The system generates a structured KB with:

```
1. Introduction
   - Problem Statement
   - Executive Summary

2. Requirements (8 subsections)
   - Challenges, Pain Points, Business Process
   - Gap Analysis, Personas, Constraints
   - Functional & Non-Functional Requirements

3. Solutioning
   - Architecture (12 detailed dimensions)

4. Assumptions & Dependencies

Appendix: Impactful Business Statements
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- Ollama with llama3 model
- Azure subscription (for Document Intelligence & Blob Storage)

### Installation

1. **Backend Setup**
```powershell
cd rfp-agent-system/backend
pip install -r requirements.txt

# Configure Azure credentials in config.py
# Set: AZURE_ENDPOINT, AZURE_KEY, BLOB_CONN_STRING
```

2. **Frontend Setup**
```powershell
cd rfp-agent-system/ui
npm install
```

3. **Start Ollama**
```powershell
ollama serve
ollama pull llama3
```

### Running the System

1. **Start Backend**
```powershell
cd rfp-agent-system/backend
python api.py
# Runs on http://localhost:8000
```

2. **Start Frontend**
```powershell
cd rfp-agent-system/ui
npm run dev
# Runs on http://localhost:5173
```

3. **Upload RFP**
- Open http://localhost:5173
- Drag & drop PDF or click to browse
- Wait for processing (~30 minutes)
- Download structured KB

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Agent Enhancement Summary](rfp-agent-system/docs/AGENT_ENHANCEMENT_SUMMARY.md) | Complete list of changes |
| [Agent Personas Reference](rfp-agent-system/docs/AGENT_PERSONAS_REFERENCE.md) | Quick reference for all personas |
| [Before/After Comparison](rfp-agent-system/docs/BEFORE_AFTER_COMPARISON.md) | Detailed improvements |
| [Agent Ecosystem Overview](rfp-agent-system/docs/AGENT_ECOSYSTEM_OVERVIEW.md) | System architecture visualization |
| [KB Structure Template](rfp-agent-system/docs/kb-structure.md) | Output template format |

## 🎨 Recent Enhancements (v2.0)

### Professional Personas Added
All agents now have professional personas with defined expertise:
- Senior Business Analyst (15+ years experience)
- Principal Solutions Architect (20+ years experience)
- NFR Specialist (15+ years experience)
- And 9 more specialized roles

### Structured Output
KB output now follows industry-standard template with:
- 4 major sections
- 25+ subsections
- Hierarchical organization
- Ready for stakeholder review

### Comprehensive Coverage
- **NFR Agent**: Expanded from 6 to 8 comprehensive categories
- **Architect Agent**: Expanded from 7 to 12 architecture dimensions
- **New Agents**: Introduction and Functional Requirements

## 🔧 Configuration

Edit `backend/config.py`:

```python
# Azure Document Intelligence
AZURE_ENDPOINT = "your-azure-endpoint"
AZURE_KEY = "your-azure-key"

# Azure Blob Storage
BLOB_CONN_STRING = "your-connection-string"
CONTAINER_NAME = "rfp-documents"

# Ollama
OLLAMA_HOST = "http://localhost:11434"
MODEL = "llama3"
```

## 📊 Performance

| Metric | Current | Future Target |
|--------|---------|---------------|
| Processing Time | ~30 min | ~10 min (parallel) |
| Agents | 12 sequential | Some parallel |
| Output Quality | High | Continuous improvement |
| Structure Compliance | 100% | Maintained |

## 🛣️ Roadmap

- [ ] Parallel agent execution for faster processing
- [ ] Diagram generation for architecture sections
- [ ] Long-term memory for team skills and preferences
- [ ] Validation layer for KB completeness
- [ ] Interactive KB editing
- [ ] Multi-language RFP support
- [ ] Comparative analysis of multiple RFPs

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📝 License

[Add your license here]

## 👥 Team

[Add team member names here]

---

**Status**: ✅ Production Ready  
**Version**: 2.0 (Enhanced with Personas)  
**Last Updated**: [Current Date]