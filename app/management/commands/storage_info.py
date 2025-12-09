"""
Django management command to show storage information.

Usage:
    python manage.py storage_info

Shows:
- Database size
- Media files size and count
- Static files size
- Log files size
- Storage breakdown by type
"""

from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from django.conf import settings
from pathlib import Path
import os
from app.models import Order, Product, OrderQRCode, HeroSlide, Customer


class Command(BaseCommand):
    help = 'Display storage information and usage statistics'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n📦 STORAGE INFORMATION REPORT'))
        self.stdout.write('=' * 70)
        self.stdout.write('')
        
        # Database size
        self._show_database_info()
        
        # Media files
        self._show_media_info()
        
        # Static files
        self._show_static_info()
        
        # Log files
        self._show_log_info()
        
        # Summary
        self._show_summary()
        
        self.stdout.write('')

    def _show_database_info(self):
        """Show database storage information"""
        self.stdout.write(self.style.SUCCESS('🗄️  DATABASE STORAGE'))
        self.stdout.write('-' * 70)
        
        # Count records
        order_count = Order.objects.count()
        product_count = Product.objects.count()
        customer_count = Customer.objects.count()
        qr_count = OrderQRCode.objects.count()
        hero_slide_count = HeroSlide.objects.count()
        
        # Estimate database size (rough calculation)
        # Each order: ~2-5 KB, Product: ~1-2 KB, Customer: ~500 bytes
        estimated_db_size = (
            order_count * 3.5 +  # Average 3.5 KB per order
            product_count * 1.5 +  # Average 1.5 KB per product
            customer_count * 0.5 +  # Average 0.5 KB per customer
            qr_count * 0.5  # Average 0.5 KB per QR record
        )
        
        # Try to get actual database file size
        db_size = 0
        db_path = None
        
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            db_path = settings.DATABASES['default']['NAME']
            if os.path.exists(db_path):
                db_size = os.path.getsize(db_path)
        elif settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            # For PostgreSQL, we can't easily get size without database query
            # Use estimated size
            db_size = estimated_db_size * 1024  # Convert KB to bytes
        
        self.stdout.write(f'  📊 Orders: {order_count:,}')
        self.stdout.write(f'  📦 Products: {product_count:,}')
        self.stdout.write(f'  👥 Customers: {customer_count:,}')
        self.stdout.write(f'  🔲 QR Codes: {qr_count:,}')
        self.stdout.write(f'  🖼️  Hero Slides: {hero_slide_count:,}')
        
        if db_size > 0:
            self.stdout.write(f'  💾 Database Size: {self._format_size(db_size)}')
        else:
            self.stdout.write(f'  💾 Estimated Database Size: {self._format_size(estimated_db_size * 1024)}')
        
        self.stdout.write('')

    def _show_media_info(self):
        """Show media files storage information"""
        self.stdout.write(self.style.SUCCESS('📁 MEDIA FILES STORAGE'))
        self.stdout.write('-' * 70)
        
        media_root = Path(settings.MEDIA_ROOT)
        
        if not media_root.exists():
            self.stdout.write('  ⚠️  Media directory does not exist')
            self.stdout.write('')
            return
        
        # Product images
        products_dir = media_root / 'products'
        products_size = 0
        products_count = 0
        if products_dir.exists():
            for file_path in products_dir.iterdir():
                if file_path.is_file():
                    products_size += file_path.stat().st_size
                    products_count += 1
        
        # QR codes
        qr_codes_dir = media_root / 'qr_codes'
        qr_codes_size = 0
        qr_codes_count = 0
        if qr_codes_dir.exists():
            for file_path in qr_codes_dir.iterdir():
                if file_path.is_file():
                    qr_codes_size += file_path.stat().st_size
                    qr_codes_count += 1
        
        # Hero slides
        hero_slides_dir = media_root / 'hero_slides'
        hero_slides_size = 0
        hero_slides_count = 0
        if hero_slides_dir.exists():
            for file_path in hero_slides_dir.rglob('*'):
                if file_path.is_file():
                    hero_slides_size += file_path.stat().st_size
                    hero_slides_count += 1
        
        total_media_size = products_size + qr_codes_size + hero_slides_size
        total_media_count = products_count + qr_codes_count + hero_slides_count
        
        self.stdout.write(f'  🖼️  Product Images: {products_count:,} files, {self._format_size(products_size)}')
        self.stdout.write(f'  🔲 QR Codes: {qr_codes_count:,} files, {self._format_size(qr_codes_size)}')
        self.stdout.write(f'  🎬 Hero Slides: {hero_slides_count:,} files, {self._format_size(hero_slides_size)}')
        self.stdout.write(f'  📊 Total Media: {total_media_count:,} files, {self._format_size(total_media_size)}')
        self.stdout.write('')

    def _show_static_info(self):
        """Show static files storage information"""
        self.stdout.write(self.style.SUCCESS('🎨 STATIC FILES STORAGE'))
        self.stdout.write('-' * 70)
        
        static_root = Path(settings.STATIC_ROOT) if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT else None
        static_dirs = settings.STATICFILES_DIRS if hasattr(settings, 'STATICFILES_DIRS') else []
        
        total_static_size = 0
        total_static_count = 0
        
        # Check staticfiles (production)
        if static_root and static_root.exists():
            for file_path in static_root.rglob('*'):
                if file_path.is_file():
                    total_static_size += file_path.stat().st_size
                    total_static_count += 1
        
        # Check static directories (development)
        for static_dir in static_dirs:
            static_path = Path(static_dir)
            if static_path.exists():
                for file_path in static_path.rglob('*'):
                    if file_path.is_file():
                        total_static_size += file_path.stat().st_size
                        total_static_count += 1
        
        self.stdout.write(f'  📊 Total Static Files: {total_static_count:,} files, {self._format_size(total_static_size)}')
        self.stdout.write('')

    def _show_log_info(self):
        """Show log files storage information"""
        self.stdout.write(self.style.SUCCESS('📝 LOG FILES STORAGE'))
        self.stdout.write('-' * 70)
        
        logs_dir = Path(settings.BASE_DIR) / 'logs'
        
        if not logs_dir.exists():
            self.stdout.write('  ⚠️  Logs directory does not exist')
            self.stdout.write('')
            return
        
        total_log_size = 0
        log_files = []
        
        for file_path in logs_dir.iterdir():
            if file_path.is_file():
                size = file_path.stat().st_size
                total_log_size += size
                log_files.append((file_path.name, size))
        
        for log_name, log_size in sorted(log_files, key=lambda x: x[1], reverse=True):
            self.stdout.write(f'  📄 {log_name}: {self._format_size(log_size)}')
        
        self.stdout.write(f'  📊 Total Logs: {self._format_size(total_log_size)}')
        self.stdout.write('')

    def _show_summary(self):
        """Show storage summary"""
        self.stdout.write(self.style.SUCCESS('📊 STORAGE SUMMARY'))
        self.stdout.write('=' * 70)
        
        # Calculate totals (rough estimates)
        media_root = Path(settings.MEDIA_ROOT)
        media_size = 0
        if media_root.exists():
            for file_path in media_root.rglob('*'):
                if file_path.is_file():
                    media_size += file_path.stat().st_size
        
        static_size = 0
        if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            static_root = Path(settings.STATIC_ROOT)
            if static_root.exists():
                for file_path in static_root.rglob('*'):
                    if file_path.is_file():
                        static_size += file_path.stat().st_size
        
        logs_dir = Path(settings.BASE_DIR) / 'logs'
        log_size = 0
        if logs_dir.exists():
            for file_path in logs_dir.iterdir():
                if file_path.is_file():
                    log_size += file_path.stat().st_size
        
        total_size = media_size + static_size + log_size
        
        self.stdout.write(f'  💾 Media Files: {self._format_size(media_size)}')
        self.stdout.write(f'  🎨 Static Files: {self._format_size(static_size)}')
        self.stdout.write(f'  📝 Log Files: {self._format_size(log_size)}')
        self.stdout.write(f'  📊 Total Storage: {self._format_size(total_size)}')
        self.stdout.write('')

    def _format_size(self, size_bytes):
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"



