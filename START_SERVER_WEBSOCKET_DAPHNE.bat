@echo off
REM ============================================
REM Start Django Server with WebSocket Support (Daphne)
REM ============================================

echo.
echo ============================================
echo Starting Django Server with WebSocket Support
echo ============================================
echo.

REM Change to the project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if daphne is installed
python -c "import daphne" 2>nul
if errorlevel 1 (
    echo Daphne not found. Installing daphne...
    pip install daphne
    if errorlevel 1 (
        echo ERROR: Failed to install daphne!
        pause
        exit /b 1
    )
)

REM Stop any existing server on port 8000
echo Checking for existing server on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Stopping existing server (PID: %%a)...
    taskkill /PID %%a /F >nul 2>&1
    if errorlevel 1 (
        echo Could not stop process %%a. You may need to stop it manually.
    ) else (
        echo Successfully stopped existing server.
    )
    timeout /t 2 /nobreak >nul
)

REM Check if Redis is running (required for WebSocket)
echo Checking Redis connection...
python -c "import redis; r = redis.Redis(host='127.0.0.1', port=6379, db=0); r.ping()" 2>nul
if errorlevel 1 (
    echo WARNING: Redis is not running or not accessible!
    echo WebSocket functionality may not work properly.
    echo Please start Redis server before continuing.
    echo.
    echo Press any key to continue anyway, or Ctrl+C to cancel...
    pause >nul
) else (
    echo Redis is running - OK
)

REM Set environment variables (if .env file exists, it will be loaded by Django)
echo.
echo Starting Daphne ASGI server...
echo Server will be available at: http://127.0.0.1:8000
echo WebSocket endpoint: ws://127.0.0.1:8000/ws/orders/
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Start Daphne with ASGI application
daphne -b 0.0.0.0 -p 8000 project.asgi:application

REM If daphne exits, show message
echo.
echo ============================================
echo Server stopped.
echo ============================================
pause

