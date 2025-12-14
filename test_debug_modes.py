"""
Test script to verify DEBUG=True and DEBUG=False both work correctly.
This script tests the Django settings configuration for both development and production modes.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text:^60}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}[OK] {text}{RESET}")

def print_error(text):
    print(f"{RED}[ERROR] {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}[WARNING] {text}{RESET}")

def print_info(text):
    print(f"{BLUE}[INFO] {text}{RESET}")

def test_settings_in_subprocess(debug_value, allowed_hosts=None):
    """Test Django settings with specific DEBUG value using subprocess."""
    print_header(f"Testing DEBUG={debug_value}")
    
    # Create test script content
    test_code = f"""
import os
import sys
from pathlib import Path

# Set environment variables BEFORE importing Django
os.environ['DEBUG'] = '{debug_value}'
"""
    if allowed_hosts:
        test_code += f"os.environ['ALLOWED_HOSTS'] = '{allowed_hosts}'\n"
    elif 'ALLOWED_HOSTS' in os.environ:
        test_code += "del os.environ['ALLOWED_HOSTS']\n"
    
    test_code += """
# Now import Django
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
django.setup()

from django.conf import settings

# Output results
print(f"DEBUG={settings.DEBUG}")
print(f"ALLOWED_HOSTS={settings.ALLOWED_HOSTS}")
print(f"SECURE_SSL_REDIRECT={getattr(settings, 'SECURE_SSL_REDIRECT', 'N/A')}")
"""
    
    # Write temporary test file
    test_file = Path(__file__).parent / 'temp_test_settings.py'
    test_file.write_text(test_code, encoding='utf-8')
    
    try:
        # Run in subprocess
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).parent),
            timeout=10
        )
        
        if result.returncode != 0:
            print_error(f"Test failed with error: {result.stderr}")
            return False
        
        # Parse output
        output_lines = result.stdout.strip().split('\n')
        actual_debug = None
        actual_hosts = None
        ssl_redirect = None
        
        for line in output_lines:
            if line.startswith('DEBUG='):
                actual_debug = line.split('=', 1)[1].strip() == 'True'
            elif line.startswith('ALLOWED_HOSTS='):
                hosts_str = line.split('=', 1)[1].strip()
                # Parse list representation
                import ast
                actual_hosts = ast.literal_eval(hosts_str)
            elif line.startswith('SECURE_SSL_REDIRECT='):
                ssl_val = line.split('=', 1)[1].strip()
                ssl_redirect = ssl_val == 'True' if ssl_val != 'N/A' else None
        
        print_info(f"DEBUG setting: {actual_debug} (expected: {debug_value})")
        print_info(f"ALLOWED_HOSTS: {actual_hosts}")
        
        if actual_debug == debug_value:
            print_success(f"DEBUG={debug_value} is correctly set")
        else:
            print_error(f"DEBUG mismatch! Expected {debug_value}, got {actual_debug}")
            return False
        
        # Check ALLOWED_HOSTS
        if debug_value:
            # DEBUG=True: Should allow all hosts or specific ones
            if '*' in actual_hosts or '127.0.0.1' in actual_hosts or 'localhost' in actual_hosts:
                print_success("ALLOWED_HOSTS configured correctly for development")
            else:
                print_warning("ALLOWED_HOSTS might be too restrictive for development")
        else:
            # DEBUG=False: Should have specific hosts
            if allowed_hosts:
                expected_hosts = [h.strip() for h in allowed_hosts.split(',') if h.strip()]
                if all(host in actual_hosts for host in expected_hosts):
                    print_success("ALLOWED_HOSTS configured correctly for production")
                else:
                    print_error(f"ALLOWED_HOSTS mismatch! Expected {expected_hosts}, got {actual_hosts}")
                    return False
            else:
                if '127.0.0.1' in actual_hosts or 'localhost' in actual_hosts:
                    print_success("ALLOWED_HOSTS has default values for production")
                else:
                    print_error("ALLOWED_HOSTS is empty in production mode!")
                    return False
        
        # Check security settings
        if not debug_value and ssl_redirect is not None:
            print_info("Checking production security settings...")
            print_info(f"SECURE_SSL_REDIRECT: {ssl_redirect}")
            if ssl_redirect:
                print_warning("HTTPS redirect is enabled (OK if behind proxy)")
            else:
                print_success("HTTPS redirect disabled (OK for local testing)")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to test settings: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up
        if test_file.exists():
            test_file.unlink()

def main():
    print_header("Django DEBUG Mode Testing")
    print_info("This script tests both DEBUG=True and DEBUG=False configurations")
    print()
    
    results = []
    
    # Test 1: DEBUG=True (Development)
    print_header("TEST 1: DEBUG=True (Development Mode)")
    result1 = test_settings_in_subprocess(True)
    results.append(("DEBUG=True", result1))
    
    # Test 2: DEBUG=False without ALLOWED_HOSTS
    print_header("TEST 2: DEBUG=False without ALLOWED_HOSTS")
    result2 = test_settings_in_subprocess(False, None)
    results.append(("DEBUG=False (no ALLOWED_HOSTS)", result2))
    
    # Test 3: DEBUG=False with ALLOWED_HOSTS
    print_header("TEST 3: DEBUG=False with ALLOWED_HOSTS")
    result3 = test_settings_in_subprocess(False, "127.0.0.1,localhost,*")
    results.append(("DEBUG=False (with ALLOWED_HOSTS)", result3))
    
    # Summary
    print_header("Test Results Summary")
    all_passed = True
    for test_name, result in results:
        if result:
            print_success(f"{test_name}: PASSED")
        else:
            print_error(f"{test_name}: FAILED")
            all_passed = False
    
    print()
    if all_passed:
        print_success("All tests passed!")
        print_info("\nYour Django settings are correctly configured for both:")
        print_info("  - Development (DEBUG=True)")
        print_info("  - Production (DEBUG=False)")
        print()
        print_info("Next steps:")
        print_info("  1. For development: Set DEBUG=True in .env")
        print_info("  2. For production: Set DEBUG=False and ALLOWED_HOSTS in .env")
        print_info("  3. Restart your server after changing settings")
        return 0
    else:
        print_error("Some tests failed!")
        print_warning("Please review the errors above and fix the configuration.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

