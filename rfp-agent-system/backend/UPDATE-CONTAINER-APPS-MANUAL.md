# Update Container Apps to Use ACR Images - Manual Steps

After Docker images are built and pushed to ACR, update each Container App:

## For Each of the 12 Container Apps:

### Container App → Image Mapping:
1. **rfp-introduction-agent** → rfp-introduction-agent:latest → AGENT_TYPE=`introduction`
2. **rfp-challenges-agent** → rfp-challenges-agent:latest → AGENT_TYPE=`challenges`
3. **rfp-pain-points-agent** → rfp-pain-points-agent:latest → AGENT_TYPE=`pain_points`
4. **rfp-business-process-agent** → rfp-business-process-agent:latest → AGENT_TYPE=`business_process`
5. **rfp-gap-agent** → rfp-gap-agent:latest → AGENT_TYPE=`gap`
6. **rfp-personas-agent** → rfp-personas-agent:latest → AGENT_TYPE=`personas`
7. **rfp-constraints-agent** → rfp-constraints-agent:latest → AGENT_TYPE=`constraints`
8. **rfp-functional-reqs-agent** → rfp-functional-reqs-agent:latest → AGENT_TYPE=`functional_requirements`
9. **rfp-nfr-agent** → rfp-nfr-agent:latest → AGENT_TYPE=`nfr`
10. **rfp-architecture-agent** → rfp-architecture-agent:latest → AGENT_TYPE=`architecture`
11. **rfp-assumptions-agent** → rfp-assumptions-agent:latest → AGENT_TYPE=`assumptions`
12. **rfp-impact-agent** → rfp-impact-agent:latest → AGENT_TYPE=`impact`

## Steps for Each Container App:

1. Go to Azure Portal → Container Apps → Select the app
2. Click **Containers** (left menu)
3. Click **Edit and deploy**
4. Click on the container name
5. Update **Container image**:
   - **Registry**: rfpenhancerregistry.azurecr.io
   - **Image**: (select matching image from dropdown)
   - **Tag**: latest
6. Go to **Environment variables** tab
7. Click **+ Add**:
   - **Name**: `AGENT_TYPE`
   - **Value**: (use the value from the mapping above - note underscores!)
8. Click **Save**
9. Click **Create** (bottom of page)
10. Wait for deployment to complete (Status shows "Running")

## Test Each Agent:

After updating, test the health endpoint:

```powershell
curl https://rfp-introduction-agent.XXXXX.eastus.azurecontainerapps.io/
```

Should return:
```json
{
  "status": "healthy",
  "agent": "introduction",
  "service": "RFP Introduction Agent"
}
```

Once all 12 are updated and tested, collect all the URLs for the next step.
