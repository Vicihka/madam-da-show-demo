@echo off
title Save Your Work
color 0A
echo ========================================
echo   SAVE YOUR WORK - Git Commit
echo ========================================
echo.

set /p MESSAGE="Enter commit message (or press Enter for default): "
if "%MESSAGE%"=="" set MESSAGE=Work saved - %date% %time%

echo.
echo Saving your work...
echo.

git add .
if errorlevel 1 (
    echo ERROR: Failed to add files!
    pause
    exit /b 1
)

git commit -m "%MESSAGE%"
if errorlevel 1 (
    echo ERROR: Failed to commit!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ WORK SAVED SUCCESSFULLY!
echo ========================================
echo.
echo Commit message: %MESSAGE%
echo.
echo Your code is now saved in Git!
echo You can safely close your computer.
echo.
pause

