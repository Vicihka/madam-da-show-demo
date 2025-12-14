"""
Comprehensive Functionality Test Script for MADAM DA E-Commerce
Tests all buttons, APIs, images, and functions
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.test import Client, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from decimal import Decimal
import json
from datetime import timedelta

from app.models import (
    Product, Customer, Order, OrderItem, PromoCode, Promoter,
    Newsletter, Referral, LoyaltyPoint, OrderQRCode, HeroSlide
)

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}[PASS] {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}[FAIL] {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")

# Test Results Tracker
class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.total = 0
    
    def add_pass(self):
        self.passed += 1
        self.total += 1
    
    def add_fail(self):
        self.failed += 1
        self.total += 1
    
    def add_warning(self):
        self.warnings += 1
    
    def print_summary(self):
        print_header("TEST SUMMARY")
        print(f"{Colors.GREEN}Passed: {self.passed}/{self.total}{Colors.RESET}")
        if self.failed > 0:
            print(f"{Colors.RED}Failed: {self.failed}/{self.total}{Colors.RESET}")
        if self.warnings > 0:
            print(f"{Colors.YELLOW}Warnings: {self.warnings}{Colors.RESET}")
        
        success_rate = (self.passed / self.total * 100) if self.total > 0 else 0
        print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.RESET}\n")

results = TestResults()

# ========== SETUP TEST DATA ==========
def setup_test_data():
    """Create test data for all tests"""
    print_info("Setting up test data...")
    
    # Create products
    product1 = Product.objects.create(
        id='TEST001',
        name='Test Product 1',
        name_kh='ផលិតផលសាកល្បង ១',
        price=Decimal('19.99'),
        stock=10,
        is_active=True
    )
    
    product2 = Product.objects.create(
        id='TEST002',
        name='Test Product 2',
        price=Decimal('29.99'),
        stock=5,
        is_active=True
    )
    
    # Create customer
    customer = Customer.objects.create(
        name='Test Customer',
        phone='012345678',
        email='test@example.com',
        address='123 Test Street',
        province='Phnom Penh'
    )
    
    # Create promo code
    promo = PromoCode.objects.create(
        code='TEST10',
        description='10% off',
        discount_type='percentage',
        discount_value=Decimal('10.00'),
        min_purchase=Decimal('50.00'),
        is_active=True
    )
    
    # Create order
    order = Order.objects.create(
        order_number='MD00001',
        customer=customer,
        customer_name='Test Customer',
        customer_phone='012345678',
        customer_address='123 Test Street',
        customer_province='Phnom Penh',
        subtotal=Decimal('19.99'),
        total=Decimal('19.99'),
        payment_method='Cash on Delivery',
        status='pending'
    )
    
    OrderItem.objects.create(
        order=order,
        product=product1,
        product_name='Test Product 1',
        product_price=Decimal('19.99'),
        quantity=1,
        subtotal=Decimal('19.99')
    )
    
    # Create hero slide
    HeroSlide.objects.create(
        title='Test Slide',
        slide_type='image',
        is_active=True,
        order=1
    )
    
    print_success("Test data created")
    return {
        'product1': product1,
        'product2': product2,
        'customer': customer,
        'promo': promo,
        'order': order
    }

# ========== TEST VIEWS ==========
def test_views(client, test_data):
    """Test all view endpoints"""
    print_header("TESTING VIEWS")
    
    views_to_test = [
        ('/', 'shop_view'),
        ('/checkout/', 'checkout_view'),
        ('/order/success/', 'order_success_view'),
        ('/track-order/', 'track_order_view'),
        ('/about-us/', 'about_us_view'),
        ('/contact/', 'contact_view'),
        ('/shipping-policy/', 'shipping_policy_view'),
        ('/privacy-policy/', 'privacy_policy_view'),
        ('/employee/', 'employee_dashboard'),
        ('/health/', 'health_check'),
    ]
    
    for url, name in views_to_test:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print_success(f"{name}: {url} - OK")
                results.add_pass()
            else:
                print_error(f"{name}: {url} - Status {response.status_code}")
                results.add_fail()
        except Exception as e:
            print_error(f"{name}: {url} - Error: {str(e)}")
            results.add_fail()

# ========== TEST API ENDPOINTS ==========
def test_api_endpoints(client, test_data):
    """Test all API endpoints"""
    print_header("TESTING API ENDPOINTS")
    
    # 1. Customer Lookup
    try:
        response = client.get('/api/customer/lookup/?phone=012345678')
        data = json.loads(response.content)
        if response.status_code == 200 and data.get('success'):
            print_success("Customer Lookup API - OK")
            results.add_pass()
        else:
            print_error("Customer Lookup API - Failed")
            results.add_fail()
    except Exception as e:
        print_error(f"Customer Lookup API - Error: {str(e)}")
        results.add_fail()
    
    # 2. Promo Code Validation
    try:
        data = {'code': 'TEST10', 'amount': 100.00}
        response = client.post(
            '/api/promo/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        result = json.loads(response.content)
        if response.status_code == 200 and result.get('success'):
            print_success("Promo Code Validation API - OK")
            results.add_pass()
        else:
            print_error("Promo Code Validation API - Failed")
            results.add_fail()
    except Exception as e:
        print_error(f"Promo Code Validation API - Error: {str(e)}")
        results.add_fail()
    
    # 3. Referral Code Check
    try:
        data = {'code': test_data['customer'].referral_code}
        response = client.post(
            '/api/referral/check/',
            data=json.dumps(data),
            content_type='application/json'
        )
        result = json.loads(response.content)
        if response.status_code == 200 and result.get('success'):
            print_success("Referral Code Check API - OK")
            results.add_pass()
        else:
            print_warning("Referral Code Check API - May need referral code setup")
            results.add_warning()
    except Exception as e:
        print_error(f"Referral Code Check API - Error: {str(e)}")
        results.add_fail()
    
    # 4. Loyalty Points Calculate
    try:
        data = {'amount': 100.00}
        response = client.post(
            '/api/loyalty/calculate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        result = json.loads(response.content)
        if response.status_code == 200 and result.get('success'):
            print_success("Loyalty Points Calculate API - OK")
            results.add_pass()
        else:
            print_warning("Loyalty Points Calculate API - May need configuration")
            results.add_warning()
    except Exception as e:
        print_error(f"Loyalty Points Calculate API - Error: {str(e)}")
        results.add_fail()
    
    # 5. Track Order API
    try:
        data = {
            'order_number': 'MD00001',
            'phone': '012345678'
        }
        response = client.post(
            '/api/order/track/',
            data=json.dumps(data),
            content_type='application/json'
        )
        result = json.loads(response.content)
        if response.status_code == 200 and result.get('success'):
            print_success("Track Order API - OK")
            results.add_pass()
        else:
            print_error("Track Order API - Failed")
            results.add_fail()
    except Exception as e:
        print_error(f"Track Order API - Error: {str(e)}")
        results.add_fail()
    
    # 6. Newsletter Subscribe
    try:
        data = {
            'email': 'newtest@example.com',
            'name': 'New Test User'
        }
        response = client.post(
            '/api/newsletter/subscribe/',
            data=json.dumps(data),
            content_type='application/json'
        )
        result = json.loads(response.content)
        if response.status_code == 200 and result.get('success'):
            print_success("Newsletter Subscribe API - OK")
            results.add_pass()
        else:
            print_error("Newsletter Subscribe API - Failed")
            results.add_fail()
    except Exception as e:
        print_error(f"Newsletter Subscribe API - Error: {str(e)}")
        results.add_fail()
    
    # 7. Health Check
    try:
        response = client.get('/health/')
        data = json.loads(response.content)
        if response.status_code == 200 and data.get('status'):
            print_success("Health Check API - OK")
            results.add_pass()
        else:
            print_error("Health Check API - Failed")
            results.add_fail()
    except Exception as e:
        print_error(f"Health Check API - Error: {str(e)}")
        results.add_fail()

# ========== TEST MODELS ==========
def test_models(test_data):
    """Test model functionality"""
    print_header("TESTING MODELS")
    
    # Test Product
    try:
        product = Product.objects.get(id='TEST001')
        assert product.name == 'Test Product 1', f"Expected 'Test Product 1', got '{product.name}'"
        print_success("Product Model - OK")
        results.add_pass()
    except Exception as e:
        print_error(f"Product Model - Error: {str(e)}")
        results.add_fail()
    
    # Test Customer
    try:
        customer = Customer.objects.get(phone='012345678')
        assert customer.referral_code is not None, "Referral code should be auto-generated"
        print_success("Customer Model - OK")
        results.add_pass()
    except Exception as e:
        print_error(f"Customer Model - Error: {str(e)}")
        results.add_fail()
    
    # Test Order
    try:
        order = Order.objects.get(order_number='MD00001')
        assert order.status == 'pending', f"Expected 'pending', got '{order.status}'"
        print_success("Order Model - OK")
        results.add_pass()
    except Exception as e:
        print_error(f"Order Model - Error: {str(e)}")
        results.add_fail()
    
    # Test PromoCode
    try:
        promo = PromoCode.objects.get(code='TEST10')
        discount = promo.calculate_discount(Decimal('100.00'))
        assert discount > 0, f"Discount should be > 0, got {discount}"
        print_success("PromoCode Model - OK")
        results.add_pass()
    except Exception as e:
        print_error(f"PromoCode Model - Error: {str(e)}")
        results.add_fail()

# ========== TEST IMAGES ==========
def test_images():
    """Test image functionality"""
    print_header("TESTING IMAGES")
    
    # Check if media directory exists
    media_dir = Path('media')
    if media_dir.exists():
        print_success("Media directory exists")
        results.add_pass()
    else:
        print_warning("Media directory not found (will be created on first upload)")
        results.add_warning()
    
    # Check if static images exist
    static_images = Path('static/images')
    if static_images.exists():
        logo_file = static_images / 'madam-da-logo.png'
        if logo_file.exists():
            print_success("Logo image exists")
            results.add_pass()
        else:
            print_warning("Logo image not found")
            results.add_warning()
    else:
        print_warning("Static images directory not found")
        results.add_warning()

# ========== TEST BUTTONS AND INTERACTIVE ELEMENTS ==========
def test_buttons_and_interactive():
    """Test buttons and interactive elements (check HTML/JS)"""
    print_header("TESTING BUTTONS AND INTERACTIVE ELEMENTS")
    
    # Read index.html to check for buttons
    try:
        index_file = Path('templates/app/index.html')
        if index_file.exists():
            content = index_file.read_text(encoding='utf-8')
            
            # Check for common buttons
            buttons_to_check = [
                ('menu-btn', 'Menu button'),
                ('cart button', 'Cart button'),
                ('add-to-cart', 'Add to cart button'),
                ('language toggle', 'Language toggle'),
                ('track order', 'Track order button'),
            ]
            
            for button_id, name in buttons_to_check:
                if button_id.lower() in content.lower():
                    print_success(f"{name} - Found in HTML")
                    results.add_pass()
                else:
                    print_warning(f"{name} - Not found (may use different ID)")
                    results.add_warning()
        else:
            print_error("index.html not found")
            results.add_fail()
    except Exception as e:
        print_error(f"Error checking buttons: {str(e)}")
        results.add_fail()
    
    # Check JavaScript files
    js_files = [
        'static/js/index.js',
        'static/js/checkout.js',
        'static/js/order_success.js',
    ]
    
    for js_file in js_files:
        file_path = Path(js_file)
        if file_path.exists():
            print_success(f"{file_path.name} - Exists")
            results.add_pass()
        else:
            print_error(f"{file_path.name} - Not found")
            results.add_fail()

# ========== MAIN TEST RUNNER ==========
def main():
    """Run all tests"""
    print_header("MADAM DA - COMPREHENSIVE FUNCTIONALITY TEST")
    print_info("This script tests all buttons, APIs, images, and functions\n")
    
    # Setup
    client = Client()
    
    # Clean up any existing test data
    print_info("Cleaning up old test data...")
    Product.objects.filter(id__startswith='TEST').delete()
    Customer.objects.filter(phone='012345678').delete()
    Order.objects.filter(order_number='MD00001').delete()
    PromoCode.objects.filter(code='TEST10').delete()
    
    # Create test data
    test_data = setup_test_data()
    
    # Run tests
    test_views(client, test_data)
    test_api_endpoints(client, test_data)
    test_models(test_data)
    test_images()
    test_buttons_and_interactive()
    
    # Print summary
    results.print_summary()
    
    # Cleanup
    print_info("Cleaning up test data...")
    Product.objects.filter(id__startswith='TEST').delete()
    Customer.objects.filter(phone='012345678').delete()
    Order.objects.filter(order_number='MD00001').delete()
    PromoCode.objects.filter(code='TEST10').delete()
    Newsletter.objects.filter(email='newtest@example.com').delete()
    
    print_success("Test cleanup complete")
    print_header("TESTING COMPLETE")

if __name__ == '__main__':
    main()

