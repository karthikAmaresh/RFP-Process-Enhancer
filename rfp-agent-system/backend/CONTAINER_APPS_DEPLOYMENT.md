# Manual Deployment Guide for Azure Container Apps
# Use this if you don't have Azure CLI installed

## Prerequisites
1. All 12 Container Apps created in Azure Portal
2. Azure Container Registry (ACR) created with Admin user enabled
3. Docker Desktop installed and running

## Step 1: Get ACR Credentials
1. Go to Azure Portal → Container registries → `rfpenhancerregistry`
2. Settings → Access keys
3. Enable "Admin user"
4. Copy:
   - Login server: `rfpenhancerregistry.azurecr.io`
   - Username: `rfpenhancerregistry`
   - Password: (copy password)

## Step 2: Login to ACR from Docker
Open PowerShell and run:
```powershell
docker login rfpenhancerregistry.azurecr.io
# Username: rfpenhancerregistry
# Password: <paste password from portal>
```

## Step 3: Build and Push Images
Run these commands one by one:

```powershell
# Navigate to backend directory
cd "C:\Users\Karthik.Amaresh\Desktop\Hackathon 2025\RFP-Process-Enhancer\rfp-agent-system\backend"

# Build and push each agent image
docker build -t rfpenhancerregistry.azurecr.io/rfp-introduction-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-introduction-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-challenges-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-challenges-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-pain_points-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-pain_points-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-business_process-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-business_process-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-gap-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-gap-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-personas-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-personas-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-constraints-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-constraints-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-functional_requirements-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-functional_requirements-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-nfr-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-nfr-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-architecture-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-architecture-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-assumptions-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-assumptions-agent:latest

docker build -t rfpenhancerregistry.azurecr.io/rfp-impact-agent:latest .
docker push rfpenhancerregistry.azurecr.io/rfp-impact-agent:latest
```

## Step 4: Update Each Container App in Portal

For each Container App, do the following:

### Example: rfp-introduction-agent

1. Go to Azure Portal → Container Apps → `rfp-introduction-agent`
2. Click **Containers** (left menu under Settings)
3. Click **Edit and deploy**
4. Click on the container name
5. Under **Container details**:
   - **Image source**: Azure Container Registry
   - **Registry**: rfpenhancerregistry
   - **Image**: rfp-introduction-agent
   - **Image tag**: latest
6. Under **Environment variables** tab, add:
   - Name: `AGENT_TYPE` | Value: `introduction`
7. Click **Save** at bottom
8. Click **Create** to deploy new revision
9. Wait for deployment to complete (Status shows "Running")

### Repeat for all 12 agents:
- `rfp-introduction-agent` → AGENT_TYPE=`introduction`
- `rfp-challenges-agent` → AGENT_TYPE=`challenges`
- `rfp-pain_points-agent` → AGENT_TYPE=`pain_points`
- `rfp-business_process-agent` → AGENT_TYPE=`business_process`
- `rfp-gap-agent` → AGENT_TYPE=`gap`
- `rfp-personas-agent` → AGENT_TYPE=`personas`
- `rfp-constraints-agent` → AGENT_TYPE=`constraints`
- `rfp-functional_requirements-agent` → AGENT_TYPE=`functional_requirements`
- `rfp-nfr-agent` → AGENT_TYPE=`nfr`
- `rfp-architecture-agent` → AGENT_TYPE=`architecture`
- `rfp-assumptions-agent` → AGENT_TYPE=`assumptions`
- `rfp-impact-agent` → AGENT_TYPE=`impact`

## Step 5: Get Container App URLs

For each Container App:
1. Go to Overview page
2. Copy the **Application Url** (e.g., `https://rfp-introduction-agent.xxx.eastus.azurecontainerapps.io`)
3. Save all 12 URLs

## Step 6: Test Each Agent

Test with curl or Postman:
```powershell
# Test introduction agent
curl -X POST "https://rfp-introduction-agent.xxx.eastus.azurecontainerapps.io/analyze" `
  -H "Content-Type: application/json" `
  -d '{"text": "This is a test RFP document about inventory management."}'
```

## Step 7: Update orchestrator.py

Once all agents are deployed and tested, update the orchestrator to call the Container App URLs instead of running locally.

---

## Troubleshooting

**Build fails with "no such file or directory":**
- Make sure you're in the backend directory when running docker build

**Push fails with authentication error:**
- Re-run `docker login rfpenhancerregistry.azurecr.io`
- Check that Admin user is enabled in ACR

**Container App shows "Failed" status:**
- Check Logs in portal: Container Apps → your app → Log stream
- Verify environment variables are set correctly
- Verify AGENT_TYPE matches the agent name

**Agent returns 500 error:**
- Check that Azure OpenAI credentials are added as environment variables
- Check Log stream for detailed error messages
