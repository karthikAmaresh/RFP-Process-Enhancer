# Quick Reference - RFP Process Enhancer

## 📁 Folder Structure
```
RFP-Process-Enhancer/
├── DEPLOYMENT.md                    # Azure Container Apps deployment guide
├── README.md                        # Main project documentation
└── rfp-agent-system/
    ├── backend/                     # Python FastAPI backend
    │   ├── .venv/                  # Python virtual environment
    │   ├── api.py                  # Main API server
    │   ├── agent_server.py         # Generic agent microservice
    │   ├── orchestrator_http.py    # HTTP orchestrator for Azure
    │   ├── Dockerfile              # Container image for agents
    │   └── rebuild-all-agents.bat  # Deploy all agents to Azure
    └── ui/                         # React frontend
        ├── src/
        ├── package.json
        └── vite.config.js
```

## 🚀 Quick Start Commands

### Local Development (Ollama)
```powershell
# Terminal 1 - Backend
cd rfp-agent-system\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn api:app --reload --port 8000

# Terminal 2 - Frontend  
cd rfp-agent-system\ui
npm run dev
```

### Azure Deployment
```cmd
cd rfp-agent-system\backend
rebuild-all-agents.bat
```

## 📖 Documentation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Project overview, features, agent ecosystem |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Azure Container Apps deployment guide |
| [QUICKSTART_UI.md](rfp-agent-system/QUICKSTART_UI.md) | UI quick start guide |
| [docs/](rfp-agent-system/docs/) | Detailed architecture and implementation docs |

## 🌐 URLs

| Service | Local | Azure |
|---------|-------|-------|
| Frontend | http://localhost:5173 | - |
| Backend API | http://localhost:8000 | - |
| Agents | Local functions | 12 Container Apps in eastus |

## 🔑 Environment Variables

Create `.env` files in backend folder:

**.env** (Main Azure services):
```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
BLOB_CONN_STRING=DefaultEndpointsProtocol=https;...
FORM_RECOGNIZER_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
FORM_RECOGNIZER_KEY=your-key
```

**.env.agents** (Auto-generated):
```
AGENT_URL_INTRODUCTION=https://rfp-introduction-agent...
AGENT_URL_CHALLENGES=https://rfp-challenges-agent...
# ... (12 total)
```

## 🛠️ Common Tasks

### Rebuild Single Agent
```cmd
cd rfp-agent-system\backend
docker build -t rfpenhancerregistry.azurecr.io/rfp-introduction-agent:latest -f Dockerfile .
docker push rfpenhancerregistry.azurecr.io/rfp-introduction-agent:latest
az containerapp update --name rfp-introduction-agent --resource-group rfp-process-enhancer --image rfpenhancerregistry.azurecr.io/rfp-introduction-agent:latest
```

### View Container App Logs
```powershell
az containerapp logs show --name rfp-introduction-agent --resource-group rfp-process-enhancer --tail 50
```

### Test Single Agent
```powershell
$body = @{text="Test RFP"; context=@{}} | ConvertTo-Json
Invoke-RestMethod -Uri "https://rfp-introduction-agent...azurecontainerapps.io/analyze" -Method POST -Body $body -ContentType "application/json"
```

## 🏗️ Architecture

**Local Mode**: Backend → Agents (in-process) → Ollama  
**Azure Mode**: Backend → HTTP → 12 Container Apps → Azure OpenAI GPT-4o

## 📋 Agent List

1. introduction - Problem statement & summary
2. challenges - Technical challenges
3. pain-points - User pain points
4. business-process - Current workflows
5. gap - Gap analysis
6. personas - User profiles
7. constraints - Constraints & limitations
8. functional-reqs - Functional requirements
9. nfr - Non-functional requirements
10. architecture - System architecture
11. assumptions - Assumptions & dependencies
12. impact - Business impact metrics

---
**Quick Help**: All commands assume you're in `RFP-Process-Enhancer` root folder.
