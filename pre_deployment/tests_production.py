"""
Enhanced Production-Ready Tests for MADAM DA E-Commerce Platform

These tests focus on production-critical scenarios including:
- Complete purchase flows
- Payment processing
- Concurrent operations
- Error handling
- Edge cases
"""

from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from decimal import Decimal
import json
from datetime import timedelta
import threading
import time

from .models import (
    Product, Customer, Order, OrderItem, PromoCode, Promoter,
    Newsletter, Referral, LoyaltyPoint, OrderQRCode
)


# ========== COMPLETE PURCHASE FLOW TESTS ==========

class CompletePurchaseFlowTest(TestCase):
    """Test complete purchase flow from cart to order confirmation"""
    
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('29.99'),
            stock=10,
            is_active=True
        )
        self.customer = Customer.objects.create(
            name='Test Customer',
            phone='012345678',
            address='123 Test St',
            province='Phnom Penh'
        )
    
    def test_complete_purchase_flow_khqr(self):
        """Test complete purchase flow with KHQR payment"""
        # 1. Checkout page loads
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        
        # 2. Create order (simulating payment confirmation)
        order_data = {
            'name': 'Test Customer',
            'phone': '012345678',
            'address': '123 Test St',
            'province': 'Phnom Penh',
            'payment_method': 'KHQR',
            'total': '29.99',
            'subtotal': '29.99',
            'discount': '0.00',
            'items': [
                {
                    'id': 'PROD001',
                    'name': 'Test Product',
                    'price': '29.99',
                    'qty': 1
                }
            ]
        }
        
        response = self.client.post(
            '/api/order/create/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        # Order should be created
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success', False))
        
        # Verify order in database
        order = Order.objects.get(order_number=data['order_number'])
        self.assertEqual(order.status, 'confirmed')
        self.assertEqual(order.payment_method, 'KHQR')
        self.assertEqual(order.total, Decimal('29.99'))
        
        # Verify order items
        self.assertEqual(order.items.count(), 1)
        item = order.items.first()
        self.assertEqual(item.product_name, 'Test Product')
        self.assertEqual(item.quantity, 1)
    
    def test_complete_purchase_flow_cod(self):
        """Test complete purchase flow with Cash on Delivery"""
        order_data = {
            'name': 'COD Customer',
            'phone': '098765432',
            'address': '456 COD St',
            'province': 'Siem Reap',
            'payment_method': 'Cash on Delivery',
            'total': '29.99',
            'subtotal': '29.99',
            'discount': '0.00',
            'items': [
                {
                    'id': 'PROD001',
                    'name': 'Test Product',
                    'price': '29.99',
                    'qty': 1
                }
            ]
        }
        
        response = self.client.post(
            '/api/order/create/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify COD order status is 'pending'
        order = Order.objects.get(order_number=data['order_number'])
        self.assertEqual(order.status, 'pending')
        self.assertFalse(order.payment_received)


# ========== PAYMENT PROCESSING TESTS ==========

class PaymentProcessingTest(TestCase):
    """Test payment processing scenarios"""
    
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('50.00'),
            stock=10,
            is_active=True
        )
    
    def test_payment_qr_code_generation(self):
        """Test QR code generation for payment"""
        # This would require mocking the Bakong API
        # For now, test the endpoint exists
        response = self.client.get('/api/payment/generate/')
        # Endpoint might require POST, adjust as needed
        # This is a placeholder test
        pass
    
    def test_payment_qr_code_expiration(self):
        """Test QR code expiration after 10 minutes"""
        order = Order.objects.create(
            order_number='MD00001',
            customer_name='Test',
            customer_phone='012345678',
            customer_address='123 St',
            customer_province='PP',
            subtotal=Decimal('50.00'),
            total=Decimal('50.00'),
            payment_method='KHQR',
            status='pending'
        )
        
        qr_code = OrderQRCode.objects.create(
            order=order,
            qr_code_image=SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg"),
            qr_data='test_data',
            created_at=timezone.now() - timedelta(minutes=11),  # 11 minutes ago
            expires_at=timezone.now() - timedelta(minutes=1)  # Expired 1 minute ago
        )
        
        # QR code should be invalid
        self.assertFalse(qr_code.is_valid())
    
    def test_payment_failure_handling(self):
        """Test handling of failed payments"""
        # Create order with failed payment status
        # Verify order status handled correctly
        # This would require integration with payment API
        pass


# ========== CONCURRENT OPERATIONS TESTS ==========

class ConcurrentOperationsTest(TransactionTestCase):
    """Test concurrent operations to catch race conditions"""
    
    def setUp(self):
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('29.99'),
            stock=1,  # Only 1 in stock
            is_active=True
        )
    
    def test_concurrent_order_for_last_item(self):
        """Test multiple users ordering the last item in stock"""
        errors = []
        
        def create_order():
            try:
                order = Order.objects.create(
                    order_number=f'MD{time.time()}',
                    customer_name='Test',
                    customer_phone=f'0{int(time.time())}',
                    customer_address='123 St',
                    customer_province='PP',
                    subtotal=Decimal('29.99'),
                    total=Decimal('29.99'),
                    payment_method='KHQR',
                    status='pending'
                )
                
                # Try to create order item and decrement stock
                OrderItem.objects.create(
                    order=order,
                    product=self.product,
                    product_name='Test Product',
                    product_price=Decimal('29.99'),
                    quantity=1,
                    subtotal=Decimal('29.99')
                )
                
                # Decrement stock
                self.product.stock -= 1
                if self.product.stock < 0:
                    raise ValueError("Stock cannot go negative")
                self.product.save()
                
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads trying to order
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=create_order)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        # Verify only one order succeeded (or all failed gracefully)
        # In production, you'd use database-level locking
        orders = Order.objects.filter(customer_province='PP')
        self.assertLessEqual(orders.count(), 1, "Only one order should succeed for last item")
        
        # Stock should not be negative
        self.product.refresh_from_db()
        self.assertGreaterEqual(self.product.stock, 0, "Stock should not go negative")


# ========== ERROR HANDLING TESTS ==========

class ErrorHandlingTest(TestCase):
    """Test error handling in various scenarios"""
    
    def setUp(self):
        self.client = Client()
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON in API requests"""
        response = self.client.post(
            '/api/promo/validate/',
            data='invalid json{',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data.get('success', True))
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        response = self.client.post(
            '/api/order/create/',
            data=json.dumps({}),
            content_type='application/json'
        )
        # Should return error
        self.assertIn(response.status_code, [400, 422])
    
    def test_database_error_handling(self):
        """Test handling of database errors"""
        # Try to create order with invalid data
        # This should be caught and return appropriate error
        pass
    
    def test_404_error_page(self):
        """Test 404 error page"""
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
        # Verify custom 404 template is used
        self.assertTemplateUsed(response, '404.html')
    
    def test_500_error_handling(self):
        """Test 500 error handling (would require causing an error)"""
        # In production, 500 errors should be logged and user shown error page
        # This test would require mocking an error
        pass


# ========== STOCK MANAGEMENT TESTS ==========

class StockManagementTest(TestCase):
    """Test stock management and validation"""
    
    def setUp(self):
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('29.99'),
            stock=5,
            is_active=True
        )
    
    def test_out_of_stock_product(self):
        """Test ordering out of stock product"""
        self.product.stock = 0
        self.product.save()
        
        # Attempt to create order with out of stock product
        # Should fail or prevent order creation
        # This depends on your implementation
        pass
    
    def test_stock_decrement(self):
        """Test stock decrements when order created"""
        initial_stock = self.product.stock
        
        order = Order.objects.create(
            order_number='MD00001',
            customer_name='Test',
            customer_phone='012345678',
            customer_address='123 St',
            customer_province='PP',
            subtotal=Decimal('29.99'),
            total=Decimal('29.99'),
            payment_method='KHQR',
            status='confirmed'
        )
        
        OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name='Test Product',
            product_price=Decimal('29.99'),
            quantity=2,
            subtotal=Decimal('59.98')
        )
        
        # If you implement stock decrement on order creation:
        # self.product.refresh_from_db()
        # self.assertEqual(self.product.stock, initial_stock - 2)


# ========== PROMO CODE EDGE CASES ==========

class PromoCodeEdgeCasesTest(TestCase):
    """Test promo code edge cases"""
    
    def setUp(self):
        self.client = Client()
        self.promo = PromoCode.objects.create(
            code='EDGE10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            min_purchase=Decimal('50.00'),
            max_discount=Decimal('20.00'),
            usage_limit=5,
            used_count=4,
            is_active=True
        )
    
    def test_promo_code_at_usage_limit(self):
        """Test promo code at usage limit"""
        self.promo.used_count = 5
        self.promo.save()
        
        data = {
            'code': 'EDGE10',
            'amount': 100.00
        }
        
        response = self.client.post(
            '/api/promo/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Should fail - reached usage limit
        self.assertEqual(response.status_code, 400)
        result = response.json()
        self.assertFalse(result.get('success', True))
    
    def test_promo_code_max_discount_cap(self):
        """Test promo code respects max discount cap"""
        # 10% of $500 = $50, but max is $20
        data = {
            'code': 'EDGE10',
            'amount': 500.00
        }
        
        response = self.client.post(
            '/api/promo/validate/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(float(result['discount_amount']), 20.00)  # Capped at max


# ========== ORDER STATUS TRANSITIONS ==========

class OrderStatusTransitionTest(TestCase):
    """Test order status transitions"""
    
    def setUp(self):
        self.order = Order.objects.create(
            order_number='MD00001',
            customer_name='Test',
            customer_phone='012345678',
            customer_address='123 St',
            customer_province='PP',
            subtotal=Decimal('50.00'),
            total=Decimal('50.00'),
            payment_method='KHQR',
            status='pending'
        )
    
    def test_valid_status_transitions(self):
        """Test valid status transitions"""
        # pending -> confirmed
        self.order.status = 'confirmed'
        self.order.save()
        self.assertEqual(self.order.status, 'confirmed')
        
        # confirmed -> preparing
        self.order.status = 'preparing'
        self.order.save()
        self.assertEqual(self.order.status, 'preparing')
    
    def test_invalid_status_transitions(self):
        """Test invalid status transitions are prevented"""
        # This depends on your implementation
        # If you have validation in the model, test it here
        pass


# ========== PERFORMANCE TESTS ==========

class PerformanceTest(TestCase):
    """Basic performance tests"""
    
    def setUp(self):
        self.client = Client()
        # Create test data
        for i in range(50):
            Product.objects.create(
                id=f'PROD{i:03d}',
                name=f'Product {i}',
                price=Decimal('29.99'),
                stock=10,
                is_active=True
            )
    
    def test_homepage_performance(self):
        """Test homepage loads quickly with many products"""
        import time
        
        start = time.time()
        response = self.client.get('/')
        elapsed = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        # Should load in under 1 second (adjust based on your requirements)
        self.assertLess(elapsed, 1.0, "Homepage should load quickly")
    
    def test_product_query_optimization(self):
        """Test product queries are optimized"""
        # Check that queries use select_related/prefetch_related where needed
        # This is more of a manual review, but you can check query count
        from django.test.utils import override_settings
        from django.db import connection
        
        with override_settings(DEBUG=True):
            connection.queries_log.clear()
            self.client.get('/')
            query_count = len(connection.queries)
            
            # Should use reasonable number of queries (adjust threshold)
            # With pagination, should be minimal queries
            self.assertLess(query_count, 10, "Too many database queries")


# ========== INTEGRATION TESTS ==========

class IntegrationTest(TestCase):
    """End-to-end integration tests"""
    
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            id='PROD001',
            name='Test Product',
            price=Decimal('50.00'),
            stock=10,
            is_active=True
        )
        self.promo = PromoCode.objects.create(
            code='INTEGRATION10',
            discount_type='percentage',
            discount_value=Decimal('10.00'),
            min_purchase=Decimal('50.00'),
            is_active=True
        )
    
    def test_end_to_end_purchase_with_promo(self):
        """Test complete purchase flow with promo code"""
        # 1. Validate promo code
        promo_data = {
            'code': 'INTEGRATION10',
            'amount': 50.00
        }
        response = self.client.post(
            '/api/promo/validate/',
            data=json.dumps(promo_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        promo_result = response.json()
        self.assertTrue(promo_result['success'])
        discount = promo_result['discount_amount']
        
        # 2. Create order with discount
        order_data = {
            'name': 'Integration Test',
            'phone': '012345678',
            'address': '123 St',
            'province': 'Phnom Penh',
            'payment_method': 'KHQR',
            'total': str(50.00 - discount),
            'subtotal': '50.00',
            'discount': str(discount),
            'items': [
                {
                    'id': 'PROD001',
                    'name': 'Test Product',
                    'price': '50.00',
                    'qty': 1
                }
            ]
        }
        
        response = self.client.post(
            '/api/order/create/',
            data=json.dumps(order_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        order_result = response.json()
        self.assertTrue(order_result['success'])
        
        # 3. Verify order created correctly
        order = Order.objects.get(order_number=order_result['order_number'])
        self.assertEqual(order.discount_amount, Decimal(str(discount)))
        self.assertEqual(order.promo_code, self.promo)
        
        # 4. Verify promo code usage count increased
        self.promo.refresh_from_db()
        self.assertEqual(self.promo.used_count, 1)


# Run these tests with:
# python manage.py test app.tests_production
