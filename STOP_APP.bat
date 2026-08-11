@echo off
title Stop GeMIntel Services
color 0C
echo =========================================================================
echo       🛑 STOPPING GEMINTEL TENDER INTELLIGENCE PLATFORM
echo =========================================================================
echo.

echo Terminating Node.js backend & frontend processes (Ports 5000, 3000)...
taskkill /F /IM node.exe 2>nul

echo Terminating Python Document Reader processes (Port 8000)...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul

echo.
echo =========================================================================
echo   ✅ All GeMIntel services stopped successfully!
echo =========================================================================
echo.
pause
