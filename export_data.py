#!/usr/bin/env python
"""Export data with proper UTF-8 encoding"""
import os
import django
import json
import sys

# Set UTF-8 encoding for stdout
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import call_command
from io import StringIO
import codecs

# Create a StringIO buffer with UTF-8 encoding
output = StringIO()

# Call dumpdata command
try:
    call_command(
        'dumpdata',
        'app',
        '--exclude', 'auth.permission',
        '--exclude', 'contenttypes',
        stdout=output
    )
    
    # Get the output
    data = output.getvalue()
    
    # Write to file with UTF-8 encoding
    with codecs.open('sqlite_backup.json', 'w', encoding='utf-8') as f:
        f.write(data)
    
    print("✅ Data exported successfully to sqlite_backup.json")
    print(f"File size: {len(data)} characters")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

