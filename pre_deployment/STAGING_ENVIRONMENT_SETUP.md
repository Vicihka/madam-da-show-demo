# 🧪 Staging Environment Setup Guide

**Purpose:** Set up a staging/test environment that mirrors production for final testing before going live.

---

## 📋 Overview

A staging environment is a replica of your production environment used for:
- Final testing before production deployment
- Testing with production-like data
- Training staff
- Demonstrating features to clients
- Testing deployment procedures

---

## 🏗️ Architecture

### Recommended Setup

```
┌─────────────────┐         ┌─────────────────┐
│   Production    │         │    Staging      │
│                 │         │                 │
│  yourdomain.com │         │ staging.domain  │
│                 │         │                 │
│  - Production DB│         │  - Staging DB   │
│  - Production   │         │  - Test Data    │
│    Redis        │         │  - Staging      │
│                 │         │    Redis        │
└─────────────────┘         └─────────────────┘
```

---

## 🛠️ Setup Steps

### 1. Server Setup

#### Option A: Separate Server (Recommended)
- Use a separate server/VPS for staging
- Same specifications as production
- Same operating system

#### Option B: Same Server, Different Domain
- Use subdomain: `staging.yourdomain.com`
- Separate database
- Separate Redis database (different DB number)

#### Option C: Local Machine (Development)
- Use for quick testing
- Not ideal for final pre-production testing

---

### 2. Database Setup

#### Create Staging Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create staging database
CREATE DATABASE madamda_staging;
CREATE USER madamda_staging_user WITH PASSWORD 'staging-password';
GRANT ALL PRIVILEGES ON DATABASE madamda_staging TO madamda_staging_user;
\q
```

#### Copy Production Data (Optional)

⚠️ **WARNING:** Only copy production data if:
- Data is anonymized (no real customer info)
- You have permission to use production data
- GDPR/privacy regulations allow it

**Method 1: Copy Database (Full Copy)**
```bash
# Dump production database
pg_dump -U madamda_user madamda_production > production_dump.sql

# Restore to staging
psql -U madamda_staging_user madamda_staging < production_dump.sql
```

**Method 2: Anonymize Data Before Copy**
```python
# create_anonymized_dump.py
from django.core.management import call_command
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Use django-anonymizer or custom script
# Anonymize customer names, emails, phone numbers
# Remove sensitive payment information
```

**Method 3: Generate Test Data**
```bash
# Create fixtures with realistic test data
python manage.py create_test_data  # Custom command
# OR use Django fixtures
python manage.py loaddata test_data.json
```

---

### 3. Environment Configuration

#### Create `.env.staging` File

```bash
# Staging Environment Variables

# Debug (can be True for easier debugging, but False recommended)
DEBUG=False

# Security
SECRET_KEY=staging-secret-key-different-from-production
ALLOWED_HOSTS=staging.yourdomain.com,staging-domain.com
CSRF_TRUSTED_ORIGINS=https://staging.yourdomain.com

# Database
DB_NAME=madamda_staging
DB_USER=madamda_staging_user
DB_PASSWORD=staging-database-password
DB_HOST=localhost
DB_PORT=5432

# Redis (use different DB number)
REDIS_URL=redis://localhost:6379/2  # DB 2 for staging (production uses 1)

# Payment API (Use TEST/SANDBOX credentials!)
BAKONG_API_BASE=https://test-bakongapi.com  # Test endpoint
BAKONG_ID=test-bakong-id
BAKONG_MERCHANT_NAME=MADAM DA (TEST)

# Telegram (optional - use test bot)
TELEGRAM_BOT_TOKEN=test-telegram-token
TELEGRAM_CHAT_ID=test-chat-id

# SSL (if using HTTPS on staging)
ENABLE_SSL_REDIRECT=True

# Admin
ADMIN_URL=admin/  # Can be same or different
```

---

### 4. Code Deployment

#### Deploy Same Code as Production

```bash
# On staging server
cd /path/to/staging
git clone <repository-url> .
# OR
git pull origin main  # If already cloned

# Activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.staging .env

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

---

### 5. Test Data Setup

#### Create Realistic Test Data

**Option 1: Django Management Command**

Create `app/management/commands/create_staging_data.py`:

```python
from django.core.management.base import BaseCommand
from app.models import Product, Customer, PromoCode, Promoter
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Create realistic test data for staging'

    def handle(self, *args, **options):
        # Create products
        products = []
        for i in range(20):
            product = Product.objects.create(
                id=f'PROD{i+1:03d}',
                name=f'Test Product {i+1}',
                name_kh=f'ផលិតផល {i+1}',
                price=Decimal(str(random.uniform(10, 100))).quantize(Decimal('0.01')),
                stock=random.randint(0, 100),
                is_active=True
            )
            products.append(product)
        
        # Create customers
        for i in range(50):
            Customer.objects.create(
                name=f'Test Customer {i+1}',
                phone=f'0{random.randint(10000000, 99999999)}',
                address=f'{random.randint(1, 999)} Test Street',
                province=random.choice(['Phnom Penh', 'Siem Reap', 'Battambang'])
            )
        
        # Create promo codes
        PromoCode.objects.create(
            code='TEST10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            min_purchase=Decimal('50.00'),
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS('Test data created successfully'))
```

Run:
```bash
python manage.py create_staging_data
```

**Option 2: Use Fixtures**

Create `fixtures/staging_data.json`:
```json
[
  {
    "model": "app.product",
    "pk": "PROD001",
    "fields": {
      "name": "Test Product 1",
      "price": "29.99",
      "stock": 50,
      "is_active": true
    }
  }
  // ... more data
]
```

Load:
```bash
python manage.py loaddata staging_data.json
```

---

### 6. Server Configuration (Nginx)

#### Staging Nginx Config

```nginx
server {
    listen 80;
    server_name staging.yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name staging.yourdomain.com;
    
    # SSL Certificate (can use self-signed for staging)
    ssl_certificate /path/to/staging-cert.pem;
    ssl_certificate_key /path/to/staging-key.pem;
    
    # Static files
    location /static/ {
        alias /path/to/staging/staticfiles/;
    }
    
    # Media files
    location /media/ {
        alias /path/to/staging/media/;
    }
    
    # Django app
    location / {
        proxy_pass http://127.0.0.1:8001;  # Different port from production
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 7. Process Management

#### Systemd Service for Staging

`/etc/systemd/system/madamda-staging.service`:

```ini
[Unit]
Description=MADAM DA Staging Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/staging
Environment="PATH=/path/to/staging/venv/bin"
EnvironmentFile=/path/to/staging/.env
ExecStart=/path/to/staging/venv/bin/gunicorn \
    --access-logfile - \
    --workers 2 \
    --bind unix:/path/to/staging/madamda-staging.sock \
    project.wsgi:application

[Install]
WantedBy=multi-user.target
```

---

### 8. Testing Workflow

#### Pre-Staging Testing Checklist

1. **Deploy to Staging**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   sudo systemctl reload madamda-staging
   ```

2. **Run Tests**
   ```bash
   python manage.py test
   ```

3. **Manual Testing**
   - Complete purchase flow
   - Test payment processing (test mode)
   - Test admin panel
   - Test all critical features

4. **Performance Testing**
   - Load testing with realistic traffic
   - Check response times
   - Monitor resource usage

5. **Security Testing**
   - Verify security headers
   - Test authentication
   - Check for vulnerabilities

---

### 9. Staging vs Production Differences

| Aspect | Staging | Production |
|--------|---------|------------|
| Domain | staging.yourdomain.com | yourdomain.com |
| Database | madamda_staging | madamda_production |
| Redis DB | 2 | 1 |
| Payment API | Test/Sandbox | Live |
| Email | Test emails (or disabled) | Real emails |
| Debug | False (or True for testing) | False |
| SSL | Self-signed OK | Valid certificate required |
| Monitoring | Basic | Full monitoring |
| Backups | Optional | Required |

---

### 10. Access Control

#### Staging Access

**Option 1: Public Access**
- Staging accessible to anyone
- Good for client demos
- ⚠️ Use test payment credentials only

**Option 2: IP Whitelist**
```nginx
# In Nginx config
location / {
    allow 1.2.3.4;  # Your IP
    allow 5.6.7.8;  # Team member IP
    deny all;
    
    proxy_pass http://127.0.0.1:8001;
}
```

**Option 3: HTTP Basic Auth**
```nginx
location / {
    auth_basic "Staging Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
    
    proxy_pass http://127.0.0.1:8001;
}
```

Create password file:
```bash
htpasswd -c /etc/nginx/.htpasswd username
```

---

### 11. Data Refresh Strategy

#### Regular Data Refresh

**Option 1: Weekly Refresh from Production**
```bash
#!/bin/bash
# refresh_staging_data.sh

# Dump production (anonymize if needed)
pg_dump -U madamda_user madamda_production > /tmp/prod_dump.sql

# Restore to staging
psql -U madamda_staging_user madamda_staging < /tmp/prod_dump.sql

# Clean up
rm /tmp/prod_dump.sql

echo "Staging data refreshed"
```

**Option 2: Regenerate Test Data**
```bash
# Clear staging database
python manage.py flush --noinput

# Regenerate test data
python manage.py create_staging_data
```

---

### 12. Monitoring Staging

#### Basic Monitoring

- **Health Check:** `https://staging.yourdomain.com/health/`
- **Error Logs:** `logs/django.log`
- **Server Logs:** `sudo journalctl -u madamda-staging`

#### Alerts (Optional)

- Set up basic uptime monitoring
- Alert on critical errors
- Monitor resource usage

---

## ✅ Staging Deployment Checklist

Before using staging for final testing:

- [ ] Staging server set up
- [ ] Database created and migrated
- [ ] Test data loaded
- [ ] Environment variables configured
- [ ] Code deployed
- [ ] Static files collected
- [ ] SSL configured (even if self-signed)
- [ ] Web server configured
- [ ] Process manager configured
- [ ] Health check working
- [ ] All tests passing
- [ ] Payment API configured (test mode)
- [ ] Access control configured
- [ ] Team notified of staging URL

---

## 🧪 Testing in Staging

### Test Scenarios

1. **Complete Purchase Flow**
   - Add products to cart
   - Checkout
   - Complete payment (test mode)
   - Verify order created

2. **Admin Panel**
   - Login
   - Create/edit products
   - Manage orders
   - Generate reports

3. **Payment Processing**
   - Test all payment methods
   - Test successful payments
   - Test failed payments
   - Test payment timeouts

4. **Edge Cases**
   - Out of stock products
   - Invalid promo codes
   - Concurrent orders
   - Large orders

5. **Performance**
   - Page load times
   - Database query performance
   - API response times

---

## 🔄 Staging to Production Promotion

Once staging is tested and approved:

1. **Final Code Review**
   - Review all changes
   - Verify tests pass
   - Check security review

2. **Deploy to Production**
   - Follow PRODUCTION_DEPLOYMENT_CHECKLIST.md
   - Deploy same code that's in staging
   - Monitor closely

3. **Post-Deployment**
   - Verify production works
   - Compare with staging behavior
   - Monitor for issues

---

## ✅ Sign-Off

**Staging Environment Ready:** ☐ Yes ☐ No  
**Tested By:** _________________  
**Date:** _________________  
**Ready for Production:** ☐ Yes ☐ No

---

**Next Steps:** Complete testing in staging, then proceed to production deployment using PRODUCTION_DEPLOYMENT_CHECKLIST.md
