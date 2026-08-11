# GeMIntel Tender Intelligence Platform - PowerShell Launcher
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host "   🚀 STARTING GEMINTEL TENDER INTELLIGENCE PLATFORM" -ForegroundColor Cyan
Write-Host "=========================================================" -ForegroundColor Cyan
Write-Host ""

$ProjectRoot = $PSScriptRoot

Write-Host "[1/3] Starting Node.js Backend Server (Port 5000)..." -ForegroundColor Yellow
Start-Process cmd.exe -ArgumentList "/k cd /d `"$ProjectRoot\backend`" && node server.js"

Start-Sleep -Seconds 2

Write-Host "[2/3] Starting Python Document Reader (Port 8000)..." -ForegroundColor Yellow
if (Test-Path "$ProjectRoot\backend\document-reader\main.py") {
    Start-Process cmd.exe -ArgumentList "/k cd /d `"$ProjectRoot\backend\document-reader`" && (python main.py || uvicorn main:app --port 8000)"
}

Start-Sleep -Seconds 2

Write-Host "[3/3] Starting React Vite Frontend App (Port 3000)..." -ForegroundColor Yellow
Start-Process cmd.exe -ArgumentList "/k cd /d `"$ProjectRoot\frontend`" && npm run dev"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "   ✅ SUCCESS! Opening Browser at http://localhost:3000" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green

Start-Process "http://localhost:3000/"
