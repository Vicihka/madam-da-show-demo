# Script to switch to PostgreSQL database
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Switch to PostgreSQL Database" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get PostgreSQL details
$DB_NAME = Read-Host "Enter PostgreSQL database name (default: madamda_db)"
if ([string]::IsNullOrWhiteSpace($DB_NAME)) { $DB_NAME = "madamda_db" }

$DB_USER = Read-Host "Enter PostgreSQL user (default: postgres)"
if ([string]::IsNullOrWhiteSpace($DB_USER)) { $DB_USER = "postgres" }

$DB_PASSWORD = Read-Host "Enter PostgreSQL password" -AsSecureString
$DB_PASSWORD_PLAIN = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($DB_PASSWORD))

$DB_HOST = Read-Host "Enter PostgreSQL host (default: localhost)"
if ([string]::IsNullOrWhiteSpace($DB_HOST)) { $DB_HOST = "localhost" }

$DB_PORT = Read-Host "Enter PostgreSQL port (default: 5432)"
if ([string]::IsNullOrWhiteSpace($DB_PORT)) { $DB_PORT = "5432" }

# Set environment variables
$env:DB_NAME = $DB_NAME
$env:DB_USER = $DB_USER
$env:DB_PASSWORD = $DB_PASSWORD_PLAIN
$env:DB_HOST = $DB_HOST
$env:DB_PORT = $DB_PORT

Write-Host ""
Write-Host "Environment variables set!" -ForegroundColor Green
Write-Host "Database: $DB_NAME" -ForegroundColor Yellow
Write-Host "User: $DB_USER" -ForegroundColor Yellow
Write-Host "Host: $DB_HOST:$DB_PORT" -ForegroundColor Yellow
Write-Host ""

# Test connection
Write-Host "Testing PostgreSQL connection..." -ForegroundColor Cyan
python -c "import psycopg2; conn = psycopg2.connect(dbname='$DB_NAME', user='$DB_USER', password='$DB_PASSWORD_PLAIN', host='$DB_HOST', port='$DB_PORT'); print('✅ Connection successful!'); conn.close()"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ PostgreSQL connection successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Now run migrations:" -ForegroundColor Cyan
    Write-Host "  python manage.py migrate" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To make these settings permanent, add them to your .env file or set them in your shell profile." -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Connection failed! Please check your PostgreSQL settings." -ForegroundColor Red
}

