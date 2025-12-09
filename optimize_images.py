"""
Advanced Image Optimization Script for MADAM DA
Converts PNG/JPG to WebP format and creates multiple sizes for responsive images.

Requirements:
    pip install Pillow

Usage:
    python optimize_images.py
"""

import os
from PIL import Image
from pathlib import Path

# Path to media folder
MEDIA_DIR = Path('static/media')

# Image sizes for responsive images
IMAGE_SIZES = {
    'small': (400, 480),   # Mobile/thumbnail
    'medium': (600, 720), # Tablet
    'large': (1200, 1440) # Desktop
}

def optimize_image(image_path, quality=85):
    """
    Optimize a single image by:
    1. Creating WebP versions in multiple sizes
    2. Creating optimized PNG versions
    3. Preserving originals
    """
    try:
        img = Image.open(image_path)
        original_size = os.path.getsize(image_path) / (1024 * 1024)  # MB
        
        # Convert RGBA to RGB if necessary (for JPEG/WebP)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        results = []
        
        # Create multiple sizes for responsive images
        for size_name, (max_width, max_height) in IMAGE_SIZES.items():
            # Resize maintaining aspect ratio
            resized_img = img.copy()
            resized_img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Create WebP version
            webp_path = image_path.parent / f"{image_path.stem}_{size_name}.webp"
            resized_img.save(webp_path, 'WEBP', quality=quality, method=6)
            webp_size = os.path.getsize(webp_path) / (1024 * 1024)
            
            # Create optimized PNG version
            png_path = image_path.parent / f"{image_path.stem}_{size_name}_optimized.png"
            resized_img.save(png_path, 'PNG', optimize=True, compress_level=9)
            png_size = os.path.getsize(png_path) / (1024 * 1024)
            
            results.append({
                'size': size_name,
                'webp': webp_size,
                'png': png_size
            })
        
        # Also create a default WebP (medium size)
        default_img = img.copy()
        default_img.thumbnail(IMAGE_SIZES['medium'], Image.Resampling.LANCZOS)
        default_webp = image_path.with_suffix('.webp')
        default_img.save(default_webp, 'WEBP', quality=quality, method=6)
        
        print(f"✓ {image_path.name}")
        print(f"  Original: {original_size:.2f} MB")
        for result in results:
            reduction = ((1 - result['webp']/original_size) * 100) if original_size > 0 else 0
            print(f"  {result['size'].capitalize()} WebP: {result['webp']:.2f} MB ({reduction:.1f}% smaller)")
        print()
        
        return True
    except Exception as e:
        print(f"✗ Error optimizing {image_path.name}: {str(e)}")
        return False

def main():
    """Optimize all images in the media folder"""
    if not MEDIA_DIR.exists():
        print(f"Error: {MEDIA_DIR} does not exist!")
        return
    
    # Get all PNG and JPG images
    image_files = list(MEDIA_DIR.glob('*.png')) + list(MEDIA_DIR.glob('*.jpg')) + list(MEDIA_DIR.glob('*.JPG')) + list(MEDIA_DIR.glob('*.jpeg')) + list(MEDIA_DIR.glob('*.JPEG'))
    
    if not image_files:
        print("No images found in static/media folder")
        return
    
    print(f"Found {len(image_files)} images to optimize...\n")
    
    optimized = 0
    for image_file in image_files:
        # Skip already optimized files
        if '_optimized' in image_file.name or '_small' in image_file.name or '_medium' in image_file.name or '_large' in image_file.name or image_file.suffix == '.webp':
            continue
        
        if optimize_image(image_file):
            optimized += 1
    
    print(f"\n✓ Optimized {optimized} images!")
    print("\nNext steps:")
    print("1. Review the optimized images")
    print("2. Templates will automatically use WebP with PNG fallbacks")
    print("3. Responsive images will load based on screen size")

if __name__ == '__main__':
    main()
