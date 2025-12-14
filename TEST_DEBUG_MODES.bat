@echo off
REM ============================================
REM Test DEBUG=True and DEBUG=False Configurations
REM ============================================

echo.
echo ============================================
echo Testing DEBUG Modes
echo ============================================
echo.

REM Change to project directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running DEBUG mode tests...
echo.

REM Run test script
python test_debug_modes.py

echo.
echo ============================================
echo Test Complete
echo ============================================
echo.
pause




