@echo off
title Check Storage Information
color 0E
echo ========================================
echo   Storage Information
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

echo [2/2] Getting storage information...
python manage.py storage_info
echo.

pause



