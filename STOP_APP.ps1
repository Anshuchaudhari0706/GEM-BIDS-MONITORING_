# GeMIntel Tender Intelligence Platform - PowerShell Stopper
Write-Host "=========================================================" -ForegroundColor Red
Write-Host "   🛑 STOPPING GEMINTEL TENDER INTELLIGENCE PLATFORM" -ForegroundColor Red
Write-Host "=========================================================" -ForegroundColor Red
Write-Host ""

Write-Host "Stopping Node.js & Vite processes..." -ForegroundColor Yellow
Stop-Process -Name "node" -Force -ErrorAction SilentlyContinue

Write-Host "Stopping Python processes..." -ForegroundColor Yellow
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "uvicorn" -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=========================================================" -ForegroundColor Green
Write-Host "   ✅ All GeMIntel services stopped successfully!" -ForegroundColor Green
Write-Host "=========================================================" -ForegroundColor Green
