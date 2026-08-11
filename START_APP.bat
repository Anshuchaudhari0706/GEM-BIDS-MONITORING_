@echo off
title GeMIntel Tender Intelligence Platform Launcher
color 0A
echo =========================================================================
echo       🚀 STARTING GEMINTEL TENDER INTELLIGENCE PLATFORM
echo =========================================================================
echo.

set "PROJECT_ROOT=%~dp0"

echo [1/3] Starting Backend Node.js Server (Port 5000)...
start "GeMIntel Backend Server (5000)" /D "%PROJECT_ROOT%backend" cmd /k "node server.js"

timeout /t 2 /nobreak >nul

echo [2/3] Starting Python Document Reader Microservice (Port 8000)...
if exist "%PROJECT_ROOT%backend\document-reader\main.py" (
    start "GeMIntel Python Reader (8000)" /D "%PROJECT_ROOT%backend\document-reader" cmd /k "python main.py || uvicorn main:app --port 8000"
)

timeout /t 2 /nobreak >nul

echo [3/3] Starting React Vite Frontend Web App (Port 3000)...
start "GeMIntel Frontend App (3000)" /D "%PROJECT_ROOT%frontend" cmd /k "npm run dev"

timeout /t 3 /nobreak >nul

echo.
echo =========================================================================
echo   ✅ SUCCESS! All Services Started. Opening Web Dashboard...
echo   App URL: http://localhost:3000
echo =========================================================================
echo.

start http://localhost:3000/

echo Keep this window open or press any key to close launcher output.
pause >nul
