# PowerShell script to set up PostgreSQL environment variables
# Run this script to configure your database connection

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Database credentials
$DB_NAME = "madamda_db"
$DB_USER = "postgres"
$DB_PASSWORD = "root"
$DB_HOST = "localhost"
$DB_PORT = "5432"

Write-Host "Setting up environment variables..." -ForegroundColor Yellow
Write-Host "Database Name: $DB_NAME" -ForegroundColor Green
Write-Host "Database User: $DB_USER" -ForegroundColor Green
Write-Host "Database Host: $DB_HOST" -ForegroundColor Green
Write-Host "Database Port: $DB_PORT" -ForegroundColor Green
Write-Host ""

# Create .env file content
$envContent = @"
# Django Settings
SECRET_KEY=django-insecure-wr-e*gp=1*s26id!o2h#tik(`$w^#olr20*8wn98aplo#wma%!u
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,*

# PostgreSQL Database Configuration
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT

# Redis (for WebSocket and caching)
REDIS_URL=redis://127.0.0.1:6379/1

# Telegram Bot (optional - set if you have)
# TELEGRAM_BOT_TOKEN=your-telegram-bot-token
# TELEGRAM_CHAT_ID=your-telegram-chat-id

# Bakong Payment (optional - set if you have)
# BAKONG_ID=your-bakong-account-id
# BAKONG_MERCHANT_NAME=MADAM DA
# BAKONG_API_BASE=https://bakongapi.com

# CSRF Trusted Origins (for production)
# CSRF_TRUSTED_ORIGINS=https://yourdomain.com
"@

# Write to .env file
$envContent | Out-File -FilePath ".env" -Encoding UTF8 -NoNewline

Write-Host "✅ .env file created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Make sure PostgreSQL is running" -ForegroundColor White
Write-Host "2. Create the database (if not exists):" -ForegroundColor White
Write-Host "   psql -U postgres -c `"CREATE DATABASE $DB_NAME;`"" -ForegroundColor Cyan
Write-Host "3. Run migrations:" -ForegroundColor White
Write-Host "   python manage.py migrate" -ForegroundColor Cyan
Write-Host "4. Test connection:" -ForegroundColor White
Write-Host "   python test_db_connection.py" -ForegroundColor Cyan
Write-Host ""





