# Update personas Container App with new image
Write-Host "Updating personas agent..." -ForegroundColor Cyan

az containerapp update `
    --name rfp-personas-agent `
    --resource-group rfp-process-enhancer `
    --image rfpenhancerregistry.azurecr.io/rfp-personas-agent:latest

Write-Host ""
Write-Host "Done! Personas agent updated." -ForegroundColor Green
