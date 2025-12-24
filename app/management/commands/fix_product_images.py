"""
Management command to fix product image paths
Usage: python manage.py fix_product_images
"""

from django.core.management.base import BaseCommand
from app.models import Product


class Command(BaseCommand):
    help = 'Fix product image paths to correct format (products/filename.ext)'

    def handle(self, *args, **options):
        products = Product.objects.all()
        fixed_count = 0
        
        for product in products:
            if product.image:
                original_path = str(product.image)
                
                # Check if path needs fixing
                needs_fix = False
                new_path = original_path
                
                # Case 1: Path starts with 'media/' or '/media/'
                if original_path.startswith('media/'):
                    new_path = original_path.replace('media/', '', 1)
                    needs_fix = True
                elif original_path.startswith('/media/'):
                    new_path = original_path.replace('/media/', '', 1)
                    needs_fix = True
                
                # Case 2: Path doesn't start with 'products/'
                elif not original_path.startswith('products/'):
                    # Extract just the filename
                    filename = original_path.split('/')[-1]
                    new_path = f'products/{filename}'
                    needs_fix = True
                
                if needs_fix:
                    product.image.name = new_path
                    product.save(update_fields=['image'])
                    fixed_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'[OK] Fixed {product.id}: {original_path} -> {new_path}'
                        )
                    )
                else:
                    self.stdout.write(
                        f'  OK {product.id}: {original_path}'
                    )
        
        if fixed_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n[SUCCESS] Fixed {fixed_count} product image(s)'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n[SUCCESS] All product images are already correct'
                )
            )

