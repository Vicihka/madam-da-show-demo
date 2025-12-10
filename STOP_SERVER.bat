@echo off
REM ============================================
REM Stop Django Server on Port 8000
REM ============================================

echo.
echo ============================================
echo Stopping Server on Port 8000
echo ============================================
echo.

REM Find and kill process on port 8000
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Found process on port 8000: PID %%a
    taskkill /PID %%a /F >nul 2>&1
    if errorlevel 1 (
        echo Failed to stop process %%a. You may need to stop it manually.
    ) else (
        echo Successfully stopped process %%a
    )
)

echo.
echo ============================================
echo Server stopped. You can now start it again.
echo ============================================
echo.
echo To start with WebSocket support:
echo   Double-click: START_SERVER_WEBSOCKET_DAPHNE.bat
echo.
echo To start without WebSocket:
echo   Double-click: START_SERVER_NORMAL.bat
echo.
pause

