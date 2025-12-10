"""
Setup Environment Variables for MADAM DA E-commerce
This script helps you create a .env file with all required variables.
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / '.env'

def generate_secret_key():
    """Generate a new Django SECRET_KEY"""
    return get_random_secret_key()

def create_env_file():
    """Create .env file with template values"""
    
    # Check if .env already exists
    if ENV_FILE.exists():
        print("\n[WARNING] .env file already exists!")
        response = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if response != 'yes':
            print("[CANCELLED] .env file not modified.")
            return False
    
    # Generate SECRET_KEY
    print("\n[INFO] Generating SECRET_KEY...")
    secret_key = generate_secret_key()
    
    # Template for .env file
    env_template = f"""# ============================================
# MADAM DA E-commerce - Environment Variables
# ============================================
# Generated automatically by setup_env.py
# 
# IMPORTANT: Never commit this file to Git!
# It's already in .gitignore
# ============================================

# ============================================
# Django Settings
# ============================================

# SECRET_KEY: Auto-generated secure key
SECRET_KEY={secret_key}

# DEBUG: Set to False in production
DEBUG=True

# ALLOWED_HOSTS: Comma-separated list of allowed hostnames
# For development: 127.0.0.1,localhost
# For production: yourdomain.com,www.yourdomain.com
ALLOWED_HOSTS=127.0.0.1,localhost

# ============================================
# Database Configuration (Optional)
# ============================================
# If not set, Django will use SQLite (db.sqlite3)
# For production, use PostgreSQL
# Uncomment and fill in if using PostgreSQL:

# DB_NAME=madamda_db
# DB_USER=postgres
# DB_PASSWORD=your_postgres_password
# DB_HOST=localhost
# DB_PORT=5432

# Alternative: Use DATABASE_URL (for cloud databases)
# DATABASE_URL=postgresql://user:password@localhost:5432/madamda_db

# ============================================
# Telegram Bot Configuration
# ============================================
# Get these from @BotFather on Telegram
# 1. Create a bot: /newbot
# 2. Get token: Copy the token provided
# 3. Get chat ID: Message your bot, then visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# ============================================
# Bakong Payment Integration
# ============================================
# Get these from your Bakong merchant account

BAKONG_ID=
BAKONG_MERCHANT_NAME=MADAM DA
BAKONG_API_BASE=https://bakongapi.com

# ============================================
# Redis Configuration (for WebSocket)
# ============================================
# Default Redis connection
# If Redis is on a different host/port, update this

REDIS_URL=redis://127.0.0.1:6379/1

# ============================================
# Security Settings (Production)
# ============================================

# CSRF Trusted Origins (for production with HTTPS)
# Add your domain here when deploying: https://yourdomain.com
# CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# CORS Allowed Origins (if you have a separate frontend)
# CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Admin URL (change from default 'admin/' for security)
# ADMIN_URL=admin/

# ============================================
# Optional: Email Configuration
# ============================================
# Uncomment and configure if you want email notifications

# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=your-email@gmail.com
"""
    
    # Write .env file
    try:
        with open(ENV_FILE, 'w', encoding='utf-8') as f:
            f.write(env_template)
        
        print(f"[SUCCESS] Successfully created .env file at: {ENV_FILE}")
        print("\n[NEXT STEPS]")
        print("   1. Open .env file in a text editor")
        print("   2. Fill in your Telegram Bot Token and Chat ID (if you have them)")
        print("   3. Fill in your Bakong ID (if you have it)")
        print("   4. Configure database settings if using PostgreSQL")
        print("\n[IMPORTANT] Remember: Never commit .env to Git!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating .env file: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("MADAM DA E-commerce - Environment Setup")
    print("=" * 60)
    
    # Set Django settings module (required for get_random_secret_key)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    
    # Import Django after setting environment
    import django
    django.setup()
    
    # Create .env file
    create_env_file()

