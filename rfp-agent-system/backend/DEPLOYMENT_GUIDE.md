# Azure Container Apps Deployment - Complete Guide

## What We've Created

1. **Dockerfile** - Single Dockerfile that works for all 12 agents
2. **agent_server.py** - Generic FastAPI server that runs any agent based on AGENT_TYPE env var
3. **orchestrator_http.py** - New orchestrator that calls agents via HTTP instead of locally
4. **build-and-push.ps1** - PowerShell script to build and push all Docker images to ACR
5. **CONTAINER_APPS_DEPLOYMENT.md** - Detailed manual deployment instructions

## Quick Start Guide

### Step 1: Build and Push Docker Images

1. Make sure Docker Desktop is running
2. Get your ACR credentials:
   - Go to Azure Portal → Container registries → `rfpenhancerregistry`
   - Settings → Access keys
   - Enable "Admin user"
   - Copy the password

3. Run the build script:
```powershell
cd "C:\Users\Karthik.Amaresh\Desktop\Hackathon 2025\RFP-Process-Enhancer\rfp-agent-system\backend"
.\build-and-push.ps1
```

4. Enter your ACR password when prompted

**This will build and push all 12 agent images to your Azure Container Registry.**

### Step 2: Update Container Apps to Use Your Images

For each of your 12 Container Apps in Azure Portal:

1. Go to Container Apps → Select the app (e.g., `rfp-introduction-agent`)
2. Click **Containers** → **Edit and deploy**
3. Click on the container name
4. Update **Image source**:
   - **Source**: Azure Container Registry
   - **Registry**: rfpenhancerregistry
   - **Image**: Select the matching image (e.g., rfp-introduction-agent)
   - **Tag**: latest
5. Go to **Environment variables** tab
6. Add new variable:
   - **Name**: `AGENT_TYPE`
   - **Value**: The agent name (e.g., `introduction`, `challenges`, etc.)
7. Click **Save** → **Create**
8. Wait for deployment (Status changes to "Running")

**Repeat for all 12 agents with their corresponding AGENT_TYPE values:**

| Container App Name | Image Name | AGENT_TYPE Value |
|-------------------|------------|------------------|
| rfp-introduction-agent | rfp-introduction-agent | `introduction` |
| rfp-challenges-agent | rfp-challenges-agent | `challenges` |
| rfp-pain_points-agent | rfp-pain_points-agent | `pain_points` |
| rfp-business_process-agent | rfp-business_process-agent | `business_process` |
| rfp-gap-agent | rfp-gap-agent | `gap` |
| rfp-personas-agent | rfp-personas-agent | `personas` |
| rfp-constraints-agent | rfp-constraints-agent | `constraints` |
| rfp-functional_requirements-agent | rfp-functional_requirements-agent | `functional_requirements` |
| rfp-nfr-agent | rfp-nfr-agent | `nfr` |
| rfp-architecture-agent | rfp-architecture-agent | `architecture` |
| rfp-assumptions-agent | rfp-assumptions-agent | `assumptions` |
| rfp-impact-agent | rfp-impact-agent | `impact` |

### Step 3: Get Container App URLs

For each Container App:
1. Go to **Overview** page
2. Copy the **Application Url** (e.g., `https://rfp-introduction-agent.xxx.eastus.azurecontainerapps.io`)
3. Save it

### Step 4: Test Each Agent

Test health endpoint:
```powershell
curl https://rfp-introduction-agent.xxx.eastus.azurecontainerapps.io/
```

Should return:
```json
{
  "status": "healthy",
  "agent": "introduction",
  "service": "RFP Introduction Agent"
}
```

Test analyze endpoint:
```powershell
curl -X POST "https://rfp-introduction-agent.xxx.eastus.azurecontainerapps.io/analyze" `
  -H "Content-Type: application/json" `
  -d '{"text": "This is a test RFP for inventory management."}'
```

### Step 5: Update Your Backend to Use Container Apps

1. Copy `.env.container-apps` to `.env.agents`:
```powershell
Copy-Item .env.container-apps .env.agents
```

2. Edit `.env.agents` and add all 12 Container App URLs:
```
AGENT_URL_INTRODUCTION=https://rfp-introduction-agent.xxx.eastus.azurecontainerapps.io
AGENT_URL_CHALLENGES=https://rfp-challenges-agent.xxx.eastus.azurecontainerapps.io
# ... etc for all 12 agents
```

3. Update `pipeline.py` to use the HTTP orchestrator:

Change:
```python
from orchestrator import run_all_agents
```

To:
```python
from orchestrator_http import run_all_agents
```

4. Load the environment variables in your app startup (in `api.py` or `config.py`):
```python
from dotenv import load_dotenv
load_dotenv('.env.agents')
```

### Step 6: Test End-to-End

1. Start your local backend:
```powershell
python -m uvicorn api:app --reload --port 8000
```

2. Upload an RFP through your frontend (http://localhost:5174)

3. Monitor the logs - you should see HTTP calls to Container Apps instead of local agent execution

## Architecture

**Before (Local):**
```
Frontend → Backend API → Local Agents → Azure OpenAI
```

**After (Container Apps):**
```
Frontend → Backend API → HTTP Calls → 12 Container Apps → Azure OpenAI
                                       (Independent microservices)
```

## Benefits

✅ **Scalability**: Each agent can scale independently based on load
✅ **Reliability**: If one agent fails, others continue working
✅ **Deployment**: Update individual agents without redeploying everything
✅ **Monitoring**: Track performance and errors per agent
✅ **Cost**: Pay only for what you use (consumption-based)

## Troubleshooting

### Docker build fails
- Make sure Docker Desktop is running
- Check that you're in the backend directory
- Verify Dockerfile syntax

### Image push fails
- Verify ACR credentials are correct
- Check Admin user is enabled in ACR Access keys
- Try `docker login rfpenhancerregistry.azurecr.io` manually

### Container App shows "Failed"
- Check **Log stream** in portal for error details
- Verify all environment variables are set (especially AGENT_TYPE)
- Check that Azure OpenAI credentials are correct

### Agent returns 500 error
- Check Container App logs
- Verify AGENT_TYPE matches the agent name exactly
- Ensure all Azure service credentials are configured

### Orchestrator can't connect to agents
- Verify Container App URLs in .env.agents are correct
- Check ingress is enabled on all Container Apps
- Test health endpoint of each agent manually

## Next Steps

Once deployed and tested:
1. ✅ Remove local agent imports from pipeline.py (optional - cleanup)
2. ✅ Add monitoring/logging for HTTP calls
3. ✅ Implement retry logic for failed HTTP calls (already done with tenacity)
4. ✅ Add health checks in your backend
5. ✅ Set up Azure Monitor alerts for agent failures
