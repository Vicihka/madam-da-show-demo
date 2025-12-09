@echo off
title Cleanup Expired QR Codes
color 0A
echo ========================================
echo   Cleanup Expired QR Codes
echo ========================================
echo.

echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [2/2] Running cleanup...
python manage.py cleanup_expired_qr_codes --days=7
echo.

pause



