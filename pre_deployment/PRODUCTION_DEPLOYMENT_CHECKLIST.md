# 🚀 Production Deployment Checklist - MADAM DA E-Commerce

**Last Updated:** 2024-01-15  
**Purpose:** Ensure smooth deployment to production with zero downtime

---

## 📋 Pre-Deployment Checklist

### ✅ 1. Code Review & Testing
- [ ] All tests passing: `python manage.py test`
- [ ] Code reviewed for security issues
- [ ] All critical bugs fixed
- [ ] Performance testing completed
- [ ] Security review completed (see SECURITY_REVIEW_PRE_DEPLOYMENT.md)
- [ ] Manual testing completed (see PRE_DEPLOYMENT_TESTING_CHECKLIST.md)
- [ ] Test scenarios completed (see TESTING_SCENARIOS.md)

### ✅ 2. Environment Variables Setup

Create `.env` file with production values:

```bash
# Required - Security
DEBUG=False
SECRET_KEY=your-very-strong-random-secret-key-here-min-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Required - Database (PostgreSQL)
DB_NAME=madamda_production
DB_USER=madamda_user
DB_PASSWORD=strong-database-password
DB_HOST=localhost
DB_PORT=5432
# OR use DATABASE_URL (preferred for cloud):
# DATABASE_URL=postgres://user:password@host:port/dbname

# Required - Redis (for caching and sessions)
REDIS_URL=redis://localhost:6379/1

# Required - Payment (Bakong)
BAKONG_API_BASE=https://bakongapi.com
BAKONG_ID=your-bakong-id
BAKONG_MERCHANT_NAME=MADAM DA

# Optional - Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id

# Optional - SSL/HTTPS
ENABLE_SSL_REDIRECT=True

# Optional - Admin Security
ADMIN_URL=custom-admin-path/  # Change from default 'admin/'
ADMIN_IP_WHITELIST=1.2.3.4,5.6.7.8  # Optional: restrict admin access

# Optional - CORS (if API accessed from different domain)
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### ✅ 3. Database Setup

#### Create Production Database

**PostgreSQL:**
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE madamda_production;
CREATE USER madamda_user WITH PASSWORD 'strong-password';
GRANT ALL PRIVILEGES ON DATABASE madamda_production TO madamda_user;
\q
```

#### Run Migrations
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Run migrations
python manage.py migrate

# Create superuser (if not exists)
python manage.py createsuperuser
```

#### Load Initial Data (if needed)
```bash
# Load fixtures (if you have any)
python manage.py loaddata initial_data.json

# Or create products via admin panel
```

---

### ✅ 4. Static Files & Media

#### Collect Static Files
```bash
# Collect all static files
python manage.py collectstatic --noinput

# Verify staticfiles directory created
ls staticfiles/
```

#### Configure Media Files
- **Option 1:** Local storage (for small deployments)
  - Ensure `media/` directory exists and is writable
  - Configure web server to serve media files

- **Option 2:** Cloud storage (recommended for production)
  - Use AWS S3, Cloudinary, or similar
  - Configure `DEFAULT_FILE_STORAGE` in settings
  - Install: `pip install django-storages boto3`

---

### ✅ 5. Server Configuration

#### Web Server Setup

**Option A: Gunicorn (WSGI)**
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Or use gunicorn_config.py
gunicorn project.wsgi:application --config gunicorn_config.py
```

**Option B: uWSGI**
```bash
pip install uwsgi
uwsgi --ini uwsgi.ini
```

#### Reverse Proxy (Nginx)

**Nginx Configuration Example:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security Headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
    
    # Static files (served by Nginx for better performance)
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files (served by Nginx or Django)
    location /media/ {
        alias /path/to/your/project/media/;
        expires 30d;
    }
    
    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

---

### ✅ 6. SSL Certificate Setup

#### Let's Encrypt (Free SSL)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx  # Ubuntu/Debian
# OR
sudo yum install certbot python3-certbot-nginx  # CentOS/RHEL

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal (already configured by certbot)
sudo certbot renew --dry-run
```

---

### ✅ 7. Process Management

#### Systemd Service (Linux)

Create `/etc/systemd/system/madamda.service`:

```ini
[Unit]
Description=MADAM DA E-Commerce Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/venv/bin"
EnvironmentFile=/path/to/your/project/.env
ExecStart=/path/to/venv/bin/gunicorn \
    --access-logfile - \
    --workers 4 \
    --bind unix:/path/to/your/project/madamda.sock \
    project.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Commands:**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start madamda

# Enable on boot
sudo systemctl enable madamda

# Check status
sudo systemctl status madamda

# View logs
sudo journalctl -u madamda -f
```

#### Supervisor (Alternative)

Create `/etc/supervisor/conf.d/madamda.conf`:

```ini
[program:madamda]
command=/path/to/venv/bin/gunicorn project.wsgi:application --bind unix:/path/to/madamda.sock
directory=/path/to/your/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/madamda/gunicorn.log
environment=PYTHONPATH="/path/to/your/project"
```

---

### ✅ 8. Redis Setup

#### Install Redis
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# CentOS/RHEL
sudo yum install redis

# Start Redis
sudo systemctl start redis
sudo systemctl enable redis
```

#### Verify Redis
```bash
redis-cli ping
# Should return: PONG
```

---

### ✅ 9. Logging Setup

#### Create Logs Directory
```bash
mkdir -p logs
chmod 755 logs
```

#### Configure Log Rotation (Optional)

Create `/etc/logrotate.d/madamda`:

```
/path/to/your/project/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

---

### ✅ 10. Backup Strategy

#### Database Backups

**Automated Backup Script:**
```bash
#!/bin/bash
# backup_database.sh

BACKUP_DIR="/path/to/backups"
DB_NAME="madamda_production"
DB_USER="madamda_user"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: db_$DATE.sql.gz"
```

**Add to Crontab:**
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup_database.sh
```

#### Media Files Backup
```bash
# Backup media directory
tar -czf /path/to/backups/media_$(date +%Y%m%d).tar.gz /path/to/media/
```

---

### ✅ 11. Monitoring & Alerts

#### Health Check Endpoint
- Already implemented: `/health/`
- Check database, cache, and system status
- Use for monitoring services (UptimeRobot, Pingdom, etc.)

#### Application Monitoring
- Consider using:
  - **Sentry** - Error tracking
  - **New Relic** - Application performance monitoring
  - **Datadog** - Infrastructure monitoring

#### Server Monitoring
- **Uptime monitoring:** UptimeRobot, Pingdom
- **Server monitoring:** Monit, Nagios, Zabbix

---

### ✅ 12. Deployment Steps

#### Initial Deployment

```bash
# 1. Clone repository (or upload files)
cd /path/to/deployment
git clone <repository-url> .
# OR upload files via FTP/SFTP

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy .env file (create with production values)
cp .env.example .env
# Edit .env with production values

# 5. Run migrations
python manage.py migrate

# 6. Collect static files
python manage.py collectstatic --noinput

# 7. Create superuser (if needed)
python manage.py createsuperuser

# 8. Test server
python manage.py runserver 0.0.0.0:8000
# Check if site works

# 9. Stop test server and start with Gunicorn
gunicorn project.wsgi:application --bind 0.0.0.0:8000

# 10. Configure systemd service (see above)
# 11. Configure Nginx (see above)
# 12. Start services
sudo systemctl start madamda
sudo systemctl restart nginx
```

#### Update Deployment (Zero Downtime)

```bash
# 1. Pull latest code
cd /path/to/deployment
git pull origin main

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install new dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Reload Gunicorn (graceful reload)
sudo systemctl reload madamda

# 7. Test site works
curl https://yourdomain.com/health/
```

---

### ✅ 13. Post-Deployment Verification

#### Check List

- [ ] **Site loads:**
  ```bash
  curl https://yourdomain.com/
  ```

- [ ] **Health check works:**
  ```bash
  curl https://yourdomain.com/health/
  ```

- [ ] **Admin panel accessible:**
  ```bash
  curl https://yourdomain.com/admin/  # Should redirect to login
  ```

- [ ] **Static files served:**
  ```bash
  curl https://yourdomain.com/static/css/index.css
  ```

- [ ] **Media files served:**
  ```bash
  curl https://yourdomain.com/media/products/product1.jpg
  ```

- [ ] **SSL certificate valid:**
  ```bash
  openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
  ```

- [ ] **Payment API works:**
  - Test payment flow in production (with test credentials first)

- [ ] **Database connectivity:**
  ```bash
  python manage.py dbshell
  # Should connect successfully
  ```

- [ ] **Redis connectivity:**
  ```bash
  redis-cli ping
  # Should return: PONG
  ```

---

### ✅ 14. Performance Optimization

#### Enable Gzip Compression
- Already handled by CompressionMiddleware
- Nginx should also compress (configure if needed)

#### Enable Browser Caching
- Static files: Already configured (1 year cache)
- Media files: 30 days cache
- HTML pages: No cache (correct)

#### Database Optimization
- [ ] Database indexes created (migrations applied)
- [ ] Query optimization checked
- [ ] Connection pooling enabled

#### CDN (Optional)
- Consider using CloudFlare or AWS CloudFront
- Offload static files to CDN

---

### ✅ 15. Security Hardening

#### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

#### Fail2Ban (Protect against brute force)
```bash
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

#### Regular Updates
```bash
# Update system packages regularly
sudo apt-get update && sudo apt-get upgrade
```

---

## 🚨 Rollback Plan

If something goes wrong:

```bash
# 1. Stop services
sudo systemctl stop madamda

# 2. Restore previous code version
cd /path/to/deployment
git checkout <previous-commit-hash>
# OR restore from backup

# 3. Restore database (if needed)
gunzip < backup.sql.gz | psql -U madamda_user madamda_production

# 4. Restore media files (if needed)
tar -xzf media_backup.tar.gz

# 5. Restart services
sudo systemctl start madamda
sudo systemctl restart nginx
```

---

## ✅ Final Checklist

Before going live:

- [ ] All pre-deployment tests passed
- [ ] Environment variables configured
- [ ] Database created and migrated
- [ ] Static files collected
- [ ] SSL certificate installed
- [ ] Web server configured
- [ ] Process manager configured (systemd/supervisor)
- [ ] Redis running
- [ ] Backups configured
- [ ] Monitoring set up
- [ ] Health check endpoint tested
- [ ] Payment processing tested (test mode first!)
- [ ] Admin panel accessible
- [ ] Error pages (404, 500) tested
- [ ] Logging working
- [ ] Security headers verified
- [ ] Firewall configured
- [ ] Team notified of deployment

---

## 📞 Support & Troubleshooting

### Common Issues

**Issue:** Site returns 500 error
- Check: `sudo journalctl -u madamda -n 50`
- Check: `tail -f logs/django.log`
- Check: `DEBUG=False` but errors not being logged properly

**Issue:** Static files not loading
- Check: `python manage.py collectstatic` ran successfully
- Check: Nginx serving static files correctly
- Check: File permissions on staticfiles directory

**Issue:** Database connection error
- Check: Database is running
- Check: Credentials in .env are correct
- Check: Database user has permissions

**Issue:** Payment not working
- Check: Bakong API credentials correct
- Check: API endpoint accessible from server
- Check: Network/firewall allows connections

---

## ✅ Sign-Off

**Deployment Completed By:** _________________  
**Date:** _________________  
**Time:** _________________  
**Status:** ☐ Success ☐ Failed  
**Site URL:** https://yourdomain.com

---

**Next Steps:**
1. Monitor logs for first 24 hours
2. Test all critical functionality
3. Monitor error rates
4. Collect user feedback

---

**🎉 Congratulations! Your e-commerce site is live!**
