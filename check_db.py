#!/usr/bin/env python
"""Check database connection and products"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.conf import settings
from django.db import connection
from app.models import Product

# Check database settings
db = settings.DATABASES['default']
print("=" * 50)
print("DATABASE CONNECTION INFO:")
print("=" * 50)
print(f"Engine: {db['ENGINE']}")
print(f"Database Name: {db['NAME']}")
print(f"Host: {db.get('HOST', 'N/A')}")
print(f"Port: {db.get('PORT', 'N/A')}")
print(f"User: {db.get('USER', 'N/A')}")
print()

# Check actual connection
print("=" * 50)
print("ACTUAL CONNECTION:")
print("=" * 50)
print(f"Database: {connection.settings_dict['NAME']}")
print(f"Host: {connection.settings_dict.get('HOST', 'N/A')}")
print()

# Check products
print("=" * 50)
print("PRODUCTS IN DATABASE:")
print("=" * 50)
products = Product.objects.all()
print(f"Total products: {products.count()}")
print()
print("All products:")
for p in products:
    print(f"  - ID: {p.id}, Name: {p.name}")
print()

# Check table name
print("=" * 50)
print("TABLE INFORMATION:")
print("=" * 50)
print(f"Product model table name: {Product._meta.db_table}")
print()

# Test direct SQL query
print("=" * 50)
print("DIRECT SQL QUERY:")
print("=" * 50)
with connection.cursor() as cursor:
    cursor.execute(f"SELECT COUNT(*) FROM {Product._meta.db_table}")
    count = cursor.fetchone()[0]
    print(f"Direct SQL count: {count}")
    print()
    cursor.execute(f"SELECT id, name FROM {Product._meta.db_table} LIMIT 5")
    rows = cursor.fetchall()
    print("First 5 products (direct SQL):")
    for row in rows:
        print(f"  - ID: {row[0]}, Name: {row[1]}")

