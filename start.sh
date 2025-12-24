#!/bin/bash

# Exit on error
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating superuser if needed..."
python manage.py create_superuser_if_none

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
gunicorn project.wsgi:application --bind 0.0.0.0:$PORT

