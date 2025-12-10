@echo off
REM ============================================
REM Start Django Server (Normal - No WebSocket)
REM ============================================

echo.
echo ============================================
echo Starting Django Server (Normal Mode)
echo ============================================
echo.
echo NOTE: This server does NOT support WebSockets.
echo For WebSocket support, use: START_SERVER_WEBSOCKET_DAPHNE.bat
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

echo.
echo Starting Django development server...
echo Server will be available at: http://127.0.0.1:8000
echo.
echo Press Ctrl+C to stop the server
echo ============================================
echo.

REM Start Django development server
python manage.py runserver

REM If server exits, show message
echo.
echo ============================================
echo Server stopped.
echo ============================================
pause

