"""
Comprehensive Unit Tests for MADAM DA E-Commerce Platform
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.paginator import Page
from decimal import Decimal
import json
from datetime import timedelta

from .models import (
    Product, Customer, Order, OrderItem, PromoCode, Promoter,
    Newsletter, Referral, LoyaltyPoint, OrderQRCode, HeroSlide
)


# ========== MODEL TESTS ==========

class ProductModelTest(TestCase):
    """Test Product model"""
    
    def setUp(self):
        """Set up test data"""
        self.product = Product.objects.create(
            id='TEST001',
            name='Test Product',
            name_kh='ផលិតផលសាកល្បង',
            description='Test description',
            description_kh='ការពិពណ៌នាសាកល្បង',
            price=Decimal('29.99'),
            old_price=Decimal('39.99'),
            stock=100,
            badge='New',
            badge_kh='ថ្មី',
            is_active=True
        )
    
    def test_product_creation(self):
        """Test product can be created"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('29.99'))
        self.assertTrue(self.product.is_active)
    
    def test_product_str(self):
        """Test product string representation"""
        self.assertEqual(str(self.product), 'Test Product')
    
    def test_product_bilingual(self):
        """Test bilingual support"""
        self.assertEqual(self.product.name_kh, 'ផលិតផលសាកល្បង')
        self.assertEqual(self.product.badge_kh, 'ថ្មី')


class CustomerModelTest(TestCase):
    """Test Customer model"""
    
    def setUp(self):
        """Set up test data"""
        self.customer = Customer.objects.create(
            name='John Doe',
            phone='012345678',
            email='john@example.com',
            address='123 Test Street',
            province='Phnom Penh'
        )
    
    def test_customer_creation(self):
        """Test customer can be created"""
        self.assertEqual(self.customer.name, 'John Doe')
        self.assertEqual(self.customer.phone, '012345678')
        self.assertIsNotNone(self.customer.referral_code)
    
    def test_customer_referral_code_generation(self):
        """Test referral code is auto-generated"""
        self.assertTrue(self.customer.referral_code.startswith('MD'))
        self.assertEqual(len(self.customer.referral_code), 8)  # MD + 6 digits
    
    def test_customer_str(self):
        """Test customer string representation"""
        self.assertIn('John Doe', str(self.customer))
        self.assertIn('012345678', str(self.customer))


class OrderModelTest(TestCase):
    """Test Order model"""
    
    def setUp(self):
        """Set up test data"""
        self.customer = Customer.objects.create(
            name='Jane Doe',
            phone='098765432',
            address='456 Test Ave',
            province='Siem Reap'
        )
        self.order = Order.objects.create(
            order_number='MD00001',
            customer=self.customer,
            customer_name='Jane Doe',
            customer_phone='098765432',
            customer_address='456 Test Ave',
            customer_province='Siem Reap',
            subtotal=Decimal('50.00'),
            total=Decimal('50.00'),
            payment_method='Cash on Delivery',
            status='pending'
        )
    
    def test_order_creation(self):
        """Test order can be created"""
        self.assertEqual(self.order.order_number, 'MD00001')
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.total, Decimal('50.00'))
    
    def test_order_status_transition(self):
        """Test order status transitions"""
        # Valid transition
        self.order.status = 'confirmed'
        self.order.save()
        self.assertEqual(self.order.status, 'confirmed')
        
        # Another valid transition
        self.order.status = 'preparing'
        self.order.save()
        self.assertEqual(self.order.status, 'preparing')
    
    def test_order_str(self):
        """Test order string representation"""
        self.assertIn('MD00001', str(self.order))
    
    def test_order_sequential_number_generation(self):
        """Test sequential order number generation"""
        order2 = Order(
            customer=self.customer,
            customer_name='Jane Doe',
            customer_phone='098765432',
            customer_address='456 Test Ave',
            customer_province='Siem Reap',
            subtotal=Decimal('30.00'),
            total=Decimal('30.00'),
            payment_method='KHQR',
            status='pending'
        )
        order2.save()
        self.assertIsNotNone(order2.order_number)
        self.assertTrue(order2.order_number.startswith('MD'))


class PromoCodeModelTest(TestCase):
    """Test PromoCode model"""
    
    def setUp(self):
        """Set up test data"""
        self.promo = PromoCode.objects.create(
            code='TEST10',
            description='10% off',
            description_kh='បញ្ចុះតម្លៃ ១០%',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            min_purchase=Decimal('50.00'),
            max_discount=Decimal('20.00'),
            is_active=True
        )
    
    def test_promo_code_creation(self):
        """Test promo code can be created"""
        self.assertEqual(self.promo.code, 'TEST10')
        self.assertEqual(self.promo.discount_type, 'percentage')
    
    def test_promo_code_is_valid(self):
        """Test promo code validation"""
        self.assertTrue(self.promo.is_valid())
    
    def test_promo_code_calculate_discount(self):
        """Test discount calculation"""
        # Test percentage discount
        discount = self.promo.calculate_discount(Decimal('100.00'))
        self.assertEqual(discount, Decimal('10.00'))  # 10% of 100
        
        # Test max discount limit
        discount = self.promo.calculate_discount(Decimal('500.00'))
        self.assertEqual(discount, Decimal('20.00'))  # Capped at max_discount
        
        # Test minimum purchase
        discount = self.promo.calculate_discount(Decimal('30.00'))
        self.assertEqual(discount, Decimal('0.00'))  # Below min_purchase


# ========== VIEW TESTS ==========

class ShopViewTest(TestCase):
    """Test shop homepage view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        # Create test products
        Product.objects.create(
            id='PROD001',
            name='Product 1',
            price=Decimal('19.99'),
            stock=10,
            is_active=True
        )
        Product.objects.create(
            id='PROD002',
            name='Product 2',
            price=Decimal('29.99'),
            stock=5,
            is_active=False  # Inactive product
        )
    
    def test_shop_view_loads(self):
        """Test shop page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertNotContains(response, 'Product 2')  # Inactive products not shown
    
    def test_shop_view_pagination(self):
        """Test pagination works"""
        # Delete existing products from setUp to avoid conflicts
        Product.objects.filter(id__startswith='PROD').delete()
        
        # Create 25 products to test pagination
        for i in range(25):
            Product.objects.create(
                id=f'PAGETEST{i:03d}',  # Use unique prefix to avoid conflicts
                name=f'Pagination Product {i}',
                price=Decimal('10.00'),
                stock=10,
                is_active=True
            )
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Should show paginated products (20 per page)
        # Check that products is a Page object (pagination is working)
        self.assertIn('products', response.context)
        self.assertIsInstance(response.context['products'], Page)
        # Verify pagination is working (should have multiple pages with 25 products)
        self.assertGreater(response.context['products'].paginator.num_pages, 1)


class CheckoutViewTest(TestCase):
    """Test checkout view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('19.99'),
            stock=10,
            is_active=True
        )
    
    def test_checkout_view_loads(self):
        """Test checkout page loads"""
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)


# ========== API TESTS ==========

class CustomerLookupAPITest(TestCase):
    """Test customer lookup API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone='012345678',
            address='123 Test St',
            province='Phnom Penh'
        )
    
    def test_customer_lookup_success(self):
        """Test successful customer lookup"""
        response = self.client.get('/api/customer/lookup/?phone=012345678')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['customer']['name'], 'Test Customer')
    
    def test_customer_lookup_not_found(self):
        """Test customer lookup when not found"""
        response = self.client.get('/api/customer/lookup/?phone=999999999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
    
    def test_customer_lookup_missing_phone(self):
        """Test customer lookup without phone"""
        response = self.client.get('/api/customer/lookup/')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


class PromoCodeValidationAPITest(TestCase):
    """Test promo code validation API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.promo = PromoCode.objects.create(
            code='TEST10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            min_purchase=Decimal('50.00'),
            is_active=True
        )
    
    def test_promo_code_validation_success(self):
        """Test successful promo code validation"""
        data = {
            'code': 'TEST10',
            'amount': 100.00
        }
        response = self.client.post(
            '/api/promo/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertEqual(float(result['discount_amount']), 10.00)
    
    def test_promo_code_validation_invalid(self):
        """Test invalid promo code"""
        data = {
            'code': 'INVALID',
            'amount': 100.00
        }
        response = self.client.post(
            '/api/promo/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
    
    def test_promo_code_below_minimum(self):
        """Test promo code with amount below minimum"""
        data = {
            'code': 'TEST10',
            'amount': 30.00  # Below min_purchase of 50.00
        }
        response = self.client.post(
            '/api/promo/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.content)
        self.assertFalse(result['success'])


class TrackOrderAPITest(TestCase):
    """Test order tracking API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone='012345678',
            address='123 Test St',
            province='Phnom Penh'
        )
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('19.99'),
            stock=10,
            is_active=True
        )
        self.order = Order.objects.create(
            order_number='MD00001',
            customer=self.customer,
            customer_name='Test Customer',
            customer_phone='012345678',
            customer_address='123 Test St',
            customer_province='Phnom Penh',
            subtotal=Decimal('19.99'),
            total=Decimal('19.99'),
            payment_method='Cash on Delivery',
            status='pending'
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name='Test Product',
            product_price=Decimal('19.99'),
            quantity=1,
            subtotal=Decimal('19.99')
        )
    
    def test_track_order_success(self):
        """Test successful order tracking"""
        data = {
            'order_number': 'MD00001',
            'phone': '012345678'
        }
        response = self.client.post(
            '/api/order/track/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertEqual(result['order']['order_number'], 'MD00001')
    
    def test_track_order_wrong_phone(self):
        """Test order tracking with wrong phone"""
        data = {
            'order_number': 'MD00001',
            'phone': '999999999'  # Wrong phone
        }
        response = self.client.post(
            '/api/order/track/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.content)
        self.assertFalse(result['success'])
    
    def test_track_order_not_found(self):
        """Test order tracking for non-existent order"""
        data = {
            'order_number': 'MD99999',
            'phone': '012345678'
        }
        response = self.client.post(
            '/api/order/track/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.content)
        self.assertFalse(result['success'])


class NewsletterSubscribeAPITest(TestCase):
    """Test newsletter subscription API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_newsletter_subscribe_success(self):
        """Test successful newsletter subscription"""
        data = {
            'email': 'test@example.com',
            'name': 'Test User'
        }
        response = self.client.post(
            '/api/newsletter/subscribe/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        
        # Verify subscription was created
        self.assertTrue(Newsletter.objects.filter(email='test@example.com').exists())
    
    def test_newsletter_subscribe_duplicate(self):
        """Test duplicate newsletter subscription"""
        Newsletter.objects.create(email='test@example.com', name='Test User')
        
        data = {
            'email': 'test@example.com',
            'name': 'Test User'
        }
        response = self.client.post(
            '/api/newsletter/subscribe/',
            data=json.dumps(data),
            content_type='application/json'
        )
        # Should still return success (idempotent)
        self.assertEqual(response.status_code, 200)


class HealthCheckAPITest(TestCase):
    """Test health check API"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_health_check_success(self):
        """Test health check endpoint"""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'ok' or data['status'] == 'degraded')
        self.assertEqual(data['database'], 'ok')


# ========== INTEGRATION TESTS ==========

class OrderFlowIntegrationTest(TestCase):
    """Test complete order flow"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('19.99'),
            stock=10,
            is_active=True
        )
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone='012345678',
            address='123 Test St',
            province='Phnom Penh'
        )
    
    def test_complete_order_flow(self):
        """Test complete order creation and tracking flow"""
        # 1. Create order
        order = Order.objects.create(
            order_number='MD00001',
            customer=self.customer,
            customer_name='Test Customer',
            customer_phone='012345678',
            customer_address='123 Test St',
            customer_province='Phnom Penh',
            subtotal=Decimal('19.99'),
            total=Decimal('19.99'),
            payment_method='Cash on Delivery',
            status='pending'
        )
        
        # 2. Add order item
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name='Test Product',
            product_price=Decimal('19.99'),
            quantity=1,
            subtotal=Decimal('19.99')
        )
        
        # 3. Track order
        data = {
            'order_number': 'MD00001',
            'phone': '012345678'
        }
        response = self.client.post(
            '/api/order/track/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content)
        self.assertTrue(result['success'])
        self.assertEqual(result['order']['status'], 'pending')


# ========== EDGE CASES AND ERROR HANDLING ==========

class ErrorHandlingTest(TestCase):
    """Test error handling"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON"""
        response = self.client.post(
            '/api/promo/validate/',
            data='invalid json',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_missing_required_fields(self):
        """Test missing required fields"""
        response = self.client.post(
            '/api/order/track/',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_404_page_not_found(self):
        """Test 404 error page"""
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
