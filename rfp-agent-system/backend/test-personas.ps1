# Test personas agent directly
Write-Host "Testing personas agent..." -ForegroundColor Cyan

$url = "https://rfp-personas-agent.greensmoke-6f577993.eastus.azurecontainerapps.io/analyze"
$body = @{
    text = "Test RFP text"
    context = @{}
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $url -Method POST -Body $body -ContentType "application/json" -TimeoutSec 60
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host "Result length: $($response.result.Length)" -ForegroundColor Cyan
} catch {
    Write-Host "FAILED!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
}
