@echo off
title Django Server with WebSocket
color 0A
echo ========================================
echo   Django Server with WebSocket Support
echo ========================================
echo.

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [2/4] Checking Redis service...
sc query Redis | find "RUNNING" >nul
if errorlevel 1 (
    echo [WARNING] Redis service not running!
    echo Attempting to start Redis...
    net start Redis >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Could not start Redis. Please start it manually.
        pause
        exit /b 1
    )
    echo [OK] Redis started
) else (
    echo [OK] Redis is running
)
echo.

echo [3/4] Installing/updating packages...
python -m pip install -q daphne channels channels-redis redis >nul 2>&1
echo [OK] Packages ready
echo.

echo [4/4] Starting server...
echo.
echo ========================================
echo   Server: http://127.0.0.1:8000
echo   Dashboard: http://127.0.0.1:8000/employee/
echo   Press Ctrl+C to stop
echo ========================================
echo.

python -m daphne -b 127.0.0.1 -p 8000 project.asgi:application
