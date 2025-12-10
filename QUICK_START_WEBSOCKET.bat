@echo off
REM ============================================
REM Quick Start: Stop Old Server & Start Daphne
REM ============================================

echo.
echo ============================================
echo Quick Start: WebSocket Server
echo ============================================
echo.

REM Change to project directory
cd /d "%~dp0"

REM Stop any existing server
echo [1/3] Stopping any existing server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
    if not errorlevel 1 (
        echo        Stopped server (PID: %%a)
    )
)
timeout /t 2 /nobreak >nul

REM Activate venv
echo [2/3] Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

REM Start Daphne
echo [3/3] Starting Daphne server with WebSocket support...
echo.
echo ============================================
echo Server starting...
echo ============================================
echo.
echo IMPORTANT: This server supports WebSockets!
echo WebSocket endpoint: ws://127.0.0.1:8000/ws/orders/
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

daphne -b 0.0.0.0 -p 8000 project.asgi:application

pause

