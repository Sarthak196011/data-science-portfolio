@echo off
title AeroPlan Prismatic Server
echo ========================================================
echo   AeroPlan Prismatic - Vivid 3D Engine & Travel API
echo ========================================================
echo.
echo Installing dependencies if needed...
pip install -r requirements.txt
echo.
echo Launching FastAPI server on http://localhost:8505...
python server.py
pause
