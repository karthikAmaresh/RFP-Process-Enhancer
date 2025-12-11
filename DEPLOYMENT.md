# RFP Process Enhancer - Azure Container Apps Deployment

## Architecture
- **Frontend**: React/Vite (localhost:5173) - Located in `rfp-agent-system/ui/`
- **Backend API**: FastAPI (localhost:8000) - Located in `rfp-agent-system/backend/`
- **Agents**: 12 Azure Container Apps (microservices)
- **AI**: Azure OpenAI GPT-4o
- **Storage**: Azure Blob Storage, Azure Document Intelligence
- **Registry**: Azure Container Registry (rfpenhancerregistry)

## Prerequisites
- Azure CLI installed and logged in
- Docker Desktop running
- Python 3.9+ with virtual environment
- Node.js for frontend

## Environment Variables Required

### Backend (.env)
```
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-15-preview
BLOB_CONN_STRING=<your-blob-connection-string>
BLOB_CONTAINER_NAME=rfp-documents
FORM_RECOGNIZER_ENDPOINT=<your-endpoint>
FORM_RECOGNIZER_KEY=<your-key>
```

### Container Apps (.env.agents) - Auto-generated
Contains URLs for all 12 Container Apps

## Deployment Steps

### 1. Initial Azure Setup (One-time)
```powershell
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name rfp-process-enhancer --location eastus

# Create Container Registry (if not exists)
az acr create --resource-group rfp-process-enhancer --name rfpenhancerregistry --sku Basic

# Login to ACR
az acr login --name rfpenhancerregistry

# Create 12 Container Apps (if not exists) - Run once
# Use Azure Portal or CLI to create:
# - rfp-introduction-agent
# - rfp-challenges-agent
# - rfp-pain-points-agent
# - rfp-business-process-agent
# - rfp-gap-agent
# - rfp-personas-agent
# - rfp-constraints-agent
# - rfp-functional-reqs-agent
# - rfp-nfr-agent
# - rfp-architecture-agent
# - rfp-assumptions-agent
# - rfp-impact-agent
```

### 2. Build and Deploy All Agents
```cmd
cd rfp-agent-system\backend
rebuild-all-agents.bat
```

This script:
- Builds Docker images for all 12 agents using the same Dockerfile
- Pushes to Azure Container Registry (rfpenhancerregistry)
- Updates all 12 Container Apps with new images
- Takes ~10-15 minutes to complete

### 3. Start Backend
```powershell
cd rfp-agent-system\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn api:app --reload --port 8000
```

### 4. Start Frontend
```powershell
cd rfp-agent-system\ui
npm run dev
```

## Files Structure

### Core Application
- `agent_server.py` - Generic FastAPI server for agents
- `orchestrator_http.py` - HTTP orchestrator calling Container Apps
- `pipeline.py` - Main RFP processing pipeline
- `api.py` - Backend REST API
- `Dockerfile` - Container image definition
- `.env.agents` - Container App URLs (auto-generated)

### Scripts
- `rebuild-all-agents.bat` - Rebuild and deploy all 12 agents to Azure

### Agent Types
Each Container App has AGENT_TYPE env var set to:
- introduction, challenges, pain_points, business_process
- gap, personas, constraints, functional_requirements
- nfr, architecture, assumptions, impact

## Usage
1. Open frontend at http://localhost:5173
2. Upload RFP document (PDF/Word)
3. Backend extracts text and calls Container Apps sequentially
4. Results displayed in frontend

## Troubleshooting

### Check Container App Logs
```powershell
az containerapp logs show --name <app-name> --resource-group rfp-process-enhancer --tail 50
```

### Rebuild Single Agent
```powershell
docker build -t rfpenhancerregistry.azurecr.io/rfp-<agent>-agent:latest -f Dockerfile .
docker push rfpenhancerregistry.azurecr.io/rfp-<agent>-agent:latest
az containerapp update --name rfp-<agent>-agent --resource-group rfp-process-enhancer --image rfpenhancerregistry.azurecr.io/rfp-<agent>-agent:latest
```

## Cost Optimization
- Container Apps scale to zero when idle
- Only pay for compute time during RFP processing
- Azure OpenAI charged per token usage

## Security
- Container Registry: Admin credentials enabled for Container Apps
- Environment variables: Set in Container App configuration
- API Keys: Never commit to source control
