@echo off
REM Quick setup script for PostgreSQL database
echo ========================================
echo PostgreSQL Database Setup
echo ========================================
echo.

echo Step 1: Creating database 'madamda_db'...
psql -U postgres -c "CREATE DATABASE madamda_db;" 2>nul
if %errorlevel% equ 0 (
    echo ✅ Database created successfully!
) else (
    echo ⚠️  Database might already exist, or there was an error.
    echo    Trying to continue anyway...
)
echo.

echo Step 2: Installing python-dotenv (if needed)...
pip install python-dotenv >nul 2>&1
echo ✅ Done
echo.

echo Step 3: Testing database connection...
python test_db_connection.py
echo.

echo Step 4: Running migrations...
python manage.py migrate
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next: Start your server with:
echo   python manage.py runserver
echo.
pause





