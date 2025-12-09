"""
Django management command to backup database.

Usage:
    python manage.py backup_database [--output=backups/]

Creates a backup of the database in JSON format.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from pathlib import Path
from datetime import datetime
import os


class Command(BaseCommand):
    help = 'Backup database to JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='backups',
            help='Output directory for backups (default: backups/)'
        )
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Compress backup file (gzip)'
        )

    def handle(self, *args, **options):
        output_dir = Path(options['output'])
        compress = options['compress']
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'db_backup_{timestamp}.json'
        if compress:
            backup_filename += '.gz'
        
        backup_path = output_dir / backup_filename
        
        self.stdout.write(self.style.SUCCESS(f'\n💾 Starting Database Backup...'))
        self.stdout.write(f'📁 Output: {backup_path}')
        self.stdout.write('')
        
        try:
            # Export database
            with open(backup_path, 'w' if not compress else 'wb') as f:
                call_command(
                    'dumpdata',
                    '--exclude', 'auth.permission',
                    '--exclude', 'contenttypes',
                    '--natural-foreign',
                    '--natural-primary',
                    stdout=f,
                    verbosity=0
                )
            
            # Get file size
            file_size = os.path.getsize(backup_path)
            
            self.stdout.write(self.style.SUCCESS('✅ Backup completed successfully!'))
            self.stdout.write(f'📊 File Size: {self._format_size(file_size)}')
            self.stdout.write(f'📁 Location: {backup_path}')
            self.stdout.write('')
            
            # Show restore instructions
            self.stdout.write(self.style.WARNING('📋 To restore this backup:'))
            self.stdout.write(f'   python manage.py loaddata {backup_path}')
            self.stdout.write('')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Backup failed: {str(e)}'))
            if backup_path.exists():
                backup_path.unlink()  # Remove partial backup
            raise

    def _format_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"



