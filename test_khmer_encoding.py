#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify Khmer text encoding
Run: python test_khmer_encoding.py
"""

import os
import sys
import io

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import Product

# Test Khmer text
khmer_text = "ផលិតផលសំអាត"

print("=" * 60)
print("Khmer Text Encoding Test")
print("=" * 60)
print(f"\n1. Test Khmer Text: {khmer_text}")
print(f"2. Text Type: {type(khmer_text)}")
print(f"3. Text Length: {len(khmer_text)}")
print(f"4. Text Bytes (UTF-8): {khmer_text.encode('utf-8')}")
print(f"5. Text Repr: {repr(khmer_text)}")

# Check if we can save to database
print("\n" + "=" * 60)
print("Database Test")
print("=" * 60)

try:
    # Get first product or create test
    product = Product.objects.first()
    if product:
        print(f"\nExisting Product: {product.name}")
        print(f"Current name_kh: {repr(product.name_kh)}")
        
        # Try to update with Khmer text
        print(f"\nUpdating with Khmer text: {khmer_text}")
        product.name_kh = khmer_text
        product.save()
        
        # Reload and check
        product.refresh_from_db()
        print(f"Saved name_kh: {repr(product.name_kh)}")
        print(f"Display name_kh: {product.name_kh}")
        
        if product.name_kh == khmer_text:
            print("✅ SUCCESS: Khmer text saved and retrieved correctly!")
        else:
            print("❌ ERROR: Khmer text was corrupted during save/retrieve")
            print(f"   Expected: {repr(khmer_text)}")
            print(f"   Got: {repr(product.name_kh)}")
    else:
        print("\nNo products found. Create a product first in admin.")
        
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

