@echo off
REM Rebuild all 12 agent Docker images and update Azure Container Apps
REM Run this from the backend directory

echo === Rebuilding All 12 Agent Images ===
echo.

set REGISTRY=rfpenhancerregistry.azurecr.io

REM Build and push all 12 images
echo [1/12] Building introduction...
docker build -t %REGISTRY%/rfp-introduction-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-introduction-agent:latest
if errorlevel 1 goto :error

echo [2/12] Building challenges...
docker build -t %REGISTRY%/rfp-challenges-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-challenges-agent:latest
if errorlevel 1 goto :error

echo [3/12] Building pain-points...
docker build -t %REGISTRY%/rfp-pain-points-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-pain-points-agent:latest
if errorlevel 1 goto :error

echo [4/12] Building business-process...
docker build -t %REGISTRY%/rfp-business-process-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-business-process-agent:latest
if errorlevel 1 goto :error

echo [5/12] Building gap...
docker build -t %REGISTRY%/rfp-gap-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-gap-agent:latest
if errorlevel 1 goto :error

echo [6/12] Building personas...
docker build -t %REGISTRY%/rfp-personas-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-personas-agent:latest
if errorlevel 1 goto :error

echo [7/12] Building constraints...
docker build -t %REGISTRY%/rfp-constraints-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-constraints-agent:latest
if errorlevel 1 goto :error

echo [8/12] Building functional-reqs...
docker build -t %REGISTRY%/rfp-functional-reqs-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-functional-reqs-agent:latest
if errorlevel 1 goto :error

echo [9/12] Building nfr...
docker build -t %REGISTRY%/rfp-nfr-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-nfr-agent:latest
if errorlevel 1 goto :error

echo [10/12] Building architecture...
docker build -t %REGISTRY%/rfp-architecture-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-architecture-agent:latest
if errorlevel 1 goto :error

echo [11/12] Building assumptions...
docker build -t %REGISTRY%/rfp-assumptions-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-assumptions-agent:latest
if errorlevel 1 goto :error

echo [12/12] Building impact...
docker build -t %REGISTRY%/rfp-impact-agent:latest -f Dockerfile .
if errorlevel 1 goto :error
docker push %REGISTRY%/rfp-impact-agent:latest
if errorlevel 1 goto :error

echo.
echo === All Images Built and Pushed Successfully! ===
echo.
echo === Updating Azure Container Apps ===
echo This will take a few minutes...
echo.

call az containerapp update --name rfp-introduction-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-introduction-agent:latest --output none
call az containerapp update --name rfp-challenges-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-challenges-agent:latest --output none
call az containerapp update --name rfp-pain-points-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-pain-points-agent:latest --output none
call az containerapp update --name rfp-business-process-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-business-process-agent:latest --output none
call az containerapp update --name rfp-gap-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-gap-agent:latest --output none
call az containerapp update --name rfp-personas-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-personas-agent:latest --output none
call az containerapp update --name rfp-constraints-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-constraints-agent:latest --output none
call az containerapp update --name rfp-functional-reqs-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-functional-reqs-agent:latest --output none
call az containerapp update --name rfp-nfr-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-nfr-agent:latest --output none
call az containerapp update --name rfp-architecture-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-architecture-agent:latest --output none
call az containerapp update --name rfp-assumptions-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-assumptions-agent:latest --output none
call az containerapp update --name rfp-impact-agent --resource-group rfp-process-enhancer --image %REGISTRY%/rfp-impact-agent:latest --output none

echo.
echo === ALL DONE! ===
echo All 12 agents deployed to Azure Container Apps
echo.
echo Next: Upload a document in your frontend to test!
goto :eof

:error
echo.
echo ERROR: Build or push failed!
echo Please check Docker is running and you're logged into ACR
exit /b 1
