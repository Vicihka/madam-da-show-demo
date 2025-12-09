#!/usr/bin/env python
"""Verify database structure"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.db import connection

# Check if customer_received column exists
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name='app_order' 
        AND column_name IN ('customer_received', 'payment_received', 'customer_received_at')
        ORDER BY column_name
    """)
    columns = cursor.fetchall()
    
    print("=" * 50)
    print("ORDER TABLE COLUMNS CHECK:")
    print("=" * 50)
    
    required_columns = ['customer_received', 'payment_received', 'customer_received_at']
    found_columns = [col[0] for col in columns]
    
    for col in required_columns:
        if col in found_columns:
            print(f"✅ {col} - EXISTS")
        else:
            print(f"❌ {col} - MISSING")
    
    if len(columns) > 0:
        print("\nAll required columns found!")
    else:
        print("\n⚠️  Some columns are missing!")

