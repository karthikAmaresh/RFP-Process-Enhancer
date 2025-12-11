# Check personas agent logs
Write-Host "Fetching logs from personas agent..." -ForegroundColor Cyan

az containerapp logs show `
    --name rfp-personas-agent `
    --resource-group rfp-process-enhancer `
    --tail 50
