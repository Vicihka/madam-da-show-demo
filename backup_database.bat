@echo off
title Backup Database
color 0B
echo ========================================
echo   Backup Database
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

echo [2/2] Creating backup...
python manage.py backup_database --compress
echo.

pause



