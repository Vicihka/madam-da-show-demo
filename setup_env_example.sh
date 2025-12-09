#!/bin/bash
# Example script to help setup environment variables
# Copy this to .env and fill in your values

echo "Creating .env file template..."

cat > .env << EOF
# Django Settings
DEBUG=False
SECRET_KEY=CHANGE_THIS_TO_GENERATED_SECRET_KEY
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,YOUR_DROPLET_IP
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database (PostgreSQL)
DATABASE_URL=postgresql://madamda_user:YOUR_DB_PASSWORD@localhost:5432/madamda_db

# Redis
REDIS_URL=redis://localhost:6379/1

# Admin Security
ADMIN_URL=secure-admin-panel/
EOF

echo ".env file created! Now edit it with: nano .env"
echo "Generate SECRET_KEY with: python manage.py shell -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""

