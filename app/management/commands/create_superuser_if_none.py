import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if none exists (for Railway deployment)'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Check if any superuser exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('✅ Superuser already exists'))
            return
        
        # Get credentials from environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not password:
            self.stdout.write(self.style.WARNING('⚠️  No DJANGO_SUPERUSER_PASSWORD set, skipping superuser creation'))
            return
        
        # Create superuser
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created successfully!'))

