"""
Test PostgreSQL Database Connection
Run this script to verify your database connection is working.
"""
import os
import sys
from pathlib import Path

# Add project directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Or set environment variables manually.")
    print()

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from django.conf import settings
from django.db import connection
from django.core.management.color import no_style

def test_connection():
    """Test database connection and display information"""
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    print()
    
    # Get database configuration
    db_config = settings.DATABASES['default']
    engine = db_config.get('ENGINE', '')
    db_name = db_config.get('NAME', '')
    db_user = db_config.get('USER', '')
    db_host = db_config.get('HOST', '')
    db_port = db_config.get('PORT', '')
    
    print("Database Configuration:")
    print(f"   Engine: {engine}")
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print()
    
    # Test connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print("[SUCCESS] Database Connection: SUCCESS")
            print(f"   PostgreSQL Version: {version}")
            print()
            
            # Check if database exists and has tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            if tables:
                print(f"Found {len(tables)} tables in database:")
                for table in tables[:10]:  # Show first 10
                    print(f"   - {table[0]}")
                if len(tables) > 10:
                    print(f"   ... and {len(tables) - 10} more")
            else:
                print("[WARNING] No tables found. Run migrations:")
                print("   python manage.py migrate")
            print()
            
            # Check connection pool info
            conn_max_age = db_config.get('CONN_MAX_AGE', 0)
            if conn_max_age > 0:
                print(f"[OK] Connection Pooling: Enabled (max age: {conn_max_age}s)")
            else:
                print("[WARNING] Connection Pooling: Disabled")
            print()
            
    except Exception as e:
        print("[ERROR] Database Connection: FAILED")
        print(f"   Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("1. Check PostgreSQL is running:")
        print("   Windows: Check Services or run 'pg_ctl status'")
        print("   Linux: sudo systemctl status postgresql")
        print()
        print("2. Verify credentials in .env file:")
        print("   DB_NAME=madamda_db")
        print("   DB_USER=postgres")
        print("   DB_PASSWORD=root")
        print("   DB_HOST=localhost")
        print("   DB_PORT=5432")
        print()
        print("3. Test connection manually:")
        print("   psql -U postgres -h localhost -d madamda_db")
        print()
        return False
    
    # Check if using PostgreSQL
    if 'postgresql' in engine.lower():
        print("[SUCCESS] Using PostgreSQL - Ready for 1000+ customers!")
    elif 'sqlite' in engine.lower():
        print("[WARNING] Using SQLite - NOT recommended for production!")
        print("   Set PostgreSQL environment variables to switch.")
    else:
        print(f"[WARNING] Using {engine} - Verify this is correct for production.")
    
    print()
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

