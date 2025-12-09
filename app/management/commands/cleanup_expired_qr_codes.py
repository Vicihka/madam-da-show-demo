"""
Django management command to cleanup expired QR codes.

Usage:
    python manage.py cleanup_expired_qr_codes [--days=7] [--dry-run]

This command removes:
- Expired QR code images (older than specified days, default 7)
- Orphaned QR code files (files without database records)
- Old tracking QR codes (older than specified days)
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.files.storage import default_storage
from datetime import timedelta
import os
from pathlib import Path

from app.models import OrderQRCode


class Command(BaseCommand):
    help = 'Cleanup expired QR codes and orphaned files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Delete QR codes older than this many days (default: 7)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force cleanup even if QR code is not expired (use with caution)'
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        force = options['force']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        self.stdout.write(self.style.SUCCESS(f'\n🧹 Starting QR Code Cleanup...'))
        self.stdout.write(f'📅 Removing QR codes older than {days} days (before {cutoff_date.strftime("%Y-%m-%d %H:%M:%S")})')
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 DRY RUN MODE - No files will be deleted'))
        self.stdout.write('')
        
        # 1. Cleanup expired OrderQRCode records
        expired_qr_codes = OrderQRCode.objects.filter(
            expires_at__lt=cutoff_date
        )
        
        deleted_count = 0
        total_size = 0
        
        for qr_code in expired_qr_codes:
            if qr_code.qr_code_image:
                file_path = qr_code.qr_code_image.path
                file_size = 0
                
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    
                    if not dry_run:
                        try:
                            # Delete the file
                            os.remove(file_path)
                            self.stdout.write(f'  ✅ Deleted: {file_path} ({self._format_size(file_size)})')
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  ❌ Error deleting {file_path}: {str(e)}'))
                    else:
                        self.stdout.write(f'  🔍 Would delete: {file_path} ({self._format_size(file_size)})')
                
                # Delete database record
                if not dry_run:
                    qr_code.delete()
                    deleted_count += 1
        
        self.stdout.write(f'\n📊 Expired QR Codes: {expired_qr_codes.count()} records')
        
        # 2. Cleanup orphaned tracking QR codes (files without database records)
        media_root = Path(default_storage.location) / 'qr_codes'
        if media_root.exists():
            tracking_files = list(media_root.glob('tracking_qr_*.png'))
            orphaned_count = 0
            
            for file_path in tracking_files:
                # Check if file is older than cutoff
                file_mtime = os.path.getmtime(file_path)
                file_date = timezone.datetime.fromtimestamp(file_mtime, tz=timezone.get_current_timezone())
                
                if file_date < cutoff_date:
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    
                    if not dry_run:
                        try:
                            os.remove(file_path)
                            self.stdout.write(f'  ✅ Deleted orphaned: {file_path.name} ({self._format_size(file_size)})')
                            orphaned_count += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  ❌ Error deleting {file_path.name}: {str(e)}'))
                    else:
                        self.stdout.write(f'  🔍 Would delete orphaned: {file_path.name} ({self._format_size(file_size)})')
                        orphaned_count += 1
        
        # 3. Cleanup old payment QR codes (qr_MD*.png) that are expired
        if media_root.exists():
            payment_files = list(media_root.glob('qr_MD*.png'))
            old_payment_count = 0
            
            for file_path in payment_files:
                # Skip if it's a tracking QR code
                if 'tracking_qr_' in file_path.name:
                    continue
                
                file_mtime = os.path.getmtime(file_path)
                file_date = timezone.datetime.fromtimestamp(file_mtime, tz=timezone.get_current_timezone())
                
                if file_date < cutoff_date:
                    # Check if QR code exists in database
                    order_number = file_path.stem.replace('qr_', '')
                    qr_exists = OrderQRCode.objects.filter(
                        order__order_number=order_number
                    ).exists()
                    
                    # Only delete if QR code is expired and not in database (or force)
                    if not qr_exists or force:
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                        
                        if not dry_run:
                            try:
                                os.remove(file_path)
                                self.stdout.write(f'  ✅ Deleted old payment QR: {file_path.name} ({self._format_size(file_size)})')
                                old_payment_count += 1
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'  ❌ Error deleting {file_path.name}: {str(e)}'))
                        else:
                            self.stdout.write(f'  🔍 Would delete old payment QR: {file_path.name} ({self._format_size(file_size)})')
                            old_payment_count += 1
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('📊 CLEANUP SUMMARY'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'🗑️  Expired QR Codes Deleted: {deleted_count}')
        self.stdout.write(f'🗑️  Orphaned Files Deleted: {orphaned_count}')
        self.stdout.write(f'🗑️  Old Payment QR Codes Deleted: {old_payment_count}')
        self.stdout.write(f'💾 Total Space Freed: {self._format_size(total_size)}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  This was a DRY RUN - No files were actually deleted'))
            self.stdout.write('   Run without --dry-run to actually delete files')
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Cleanup completed successfully!'))
        
        self.stdout.write('')

    def _format_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"



