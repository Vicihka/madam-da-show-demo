@echo off
REM ============================================
REM Setup Environment Variables for MADAM DA
REM ============================================

echo.
echo ============================================
echo MADAM DA - Environment Setup
echo ============================================
echo.

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

REM Check if Django is installed
python -c "import django" 2>nul
if errorlevel 1 (
    echo ERROR: Django is not installed!
    echo Please install requirements:
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

REM Run setup script
echo.
echo Running environment setup...
python setup_env.py

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
pause

