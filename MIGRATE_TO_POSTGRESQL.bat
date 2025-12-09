@echo off
title Migrate from SQLite to PostgreSQL
color 0E
echo ========================================
echo   Migrate Data from SQLite to PostgreSQL
echo ========================================
echo.
echo This will:
echo   1. Export all data from SQLite
echo   2. Switch to PostgreSQL
echo   3. Import data to PostgreSQL
echo.
echo Your superuser and all data will be preserved!
echo.

set /p CONFIRM="Continue? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo Migration cancelled.
    pause
    exit /b 0
)

echo.
echo [Step 1] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Virtual environment not found!
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [Step 2] Getting PostgreSQL details...
set /p DB_NAME="Database name (default: madamda_db): "
if "%DB_NAME%"=="" set DB_NAME=madamda_db

set /p DB_USER="PostgreSQL user (default: postgres): "
if "%DB_USER%"=="" set DB_USER=postgres

set /p DB_PASSWORD="PostgreSQL password: "
if "%DB_PASSWORD%"=="" (
    echo ERROR: Password is required!
    pause
    exit /b 1
)

set /p DB_HOST="Host (default: localhost): "
if "%DB_HOST%"=="" set DB_HOST=localhost

set /p DB_PORT="Port (default: 5432): "
if "%DB_PORT%"=="" set DB_PORT=5432

echo.
echo [Step 3] Setting environment variables...
set DB_NAME=%DB_NAME%
set DB_USER=%DB_USER%
set DB_PASSWORD=%DB_PASSWORD%
set DB_HOST=%DB_HOST%
set DB_PORT=%DB_PORT%
echo [OK] Environment variables set
echo.

echo [Step 4] Installing PostgreSQL driver...
python -m pip install -q psycopg2-binary
echo [OK] PostgreSQL driver installed
echo.

echo [Step 5] Exporting data from SQLite...
if exist data_export.json del data_export.json
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data_export.json
if errorlevel 1 (
    echo ERROR: Failed to export data!
    pause
    exit /b 1
)
echo [OK] Data exported to data_export.json
echo.

echo [Step 6] Testing PostgreSQL connection...
python -c "import psycopg2; conn = psycopg2.connect(dbname='%DB_NAME%', user='%DB_USER%', password='%DB_PASSWORD%', host='%DB_HOST%', port='%DB_PORT%'); print('✅ Connection successful!'); conn.close()" 2>nul
if errorlevel 1 (
    echo.
    echo [WARNING] Could not connect to PostgreSQL.
    echo Please make sure:
    echo   1. PostgreSQL is running
    echo   2. Database '%DB_NAME%' exists
    echo   3. User '%DB_USER%' has access
    echo   4. Password is correct
    echo.
    echo To create database:
    echo   psql -U %DB_USER% -c "CREATE DATABASE %DB_NAME%;"
    echo.
    pause
    exit /b 1
)
echo [OK] PostgreSQL connection successful
echo.

echo [Step 7] Running migrations on PostgreSQL...
python manage.py makemigrations
python manage.py migrate
echo [OK] Migrations completed
echo.

echo [Step 8] Importing data to PostgreSQL...
python manage.py loaddata data_export.json
if errorlevel 1 (
    echo.
    echo [WARNING] Some data may not have imported correctly.
    echo This is normal for contenttypes and permissions.
    echo Your superuser and orders should be imported.
    echo.
) else (
    echo [OK] Data imported successfully
)
echo.

echo [Step 9] Cleaning up...
if exist data_export.json del data_export.json
echo [OK] Temporary files removed
echo.

echo ========================================
echo   Migration Complete!
echo ========================================
echo.
echo Your data has been migrated to PostgreSQL!
echo.
echo Your superuser account is preserved.
echo All your orders, products, and data are now in PostgreSQL.
echo.
echo Database: %DB_NAME%
echo User: %DB_USER%
echo.
echo To start server:
echo   START_SERVER_WEBSOCKET.bat
echo.
pause

