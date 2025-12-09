from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from datetime import timedelta
import uuid
import os


def validate_video_file(value):
    """Validate uploaded video file"""
    max_size = 50 * 1024 * 1024  # 50MB
    if value.size > max_size:
        raise ValidationError(f'Video file too large. Maximum size is {max_size / 1024 / 1024}MB.')
    
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.mp4', '.webm', '.mov']
    if ext not in allowed_extensions:
        raise ValidationError(f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}')


def validate_image_file(value):
    """Validate uploaded image file"""
    # Check file size (5MB max)
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(f'Image file too large. Maximum size is {max_size / 1024 / 1024}MB.')
    
    # Check file extension
    ext = os.path.splitext(value.name)[1].lower()
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
    if ext not in allowed_extensions:
        raise ValidationError(f'Invalid file type. Allowed types: {", ".join(allowed_extensions)}')
    
    # Check MIME type (basic check)
    if hasattr(value, 'content_type'):
        allowed_mimes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
        if value.content_type not in allowed_mimes:
            raise ValidationError('Invalid file type. Only image files are allowed.')


class Product(models.Model):
    """Product model for beauty products"""
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    name_kh = models.CharField(max_length=200, blank=True, null=True, help_text="Khmer name")
    description = models.TextField(blank=True, null=True)
    description_kh = models.TextField(blank=True, null=True, help_text="Khmer description")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    image = models.ImageField(
        upload_to='products/', 
        help_text="Product image",
        validators=[validate_image_file, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'])]
    )
    badge = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 'New', 'Sale', 'Popular'")
    badge_kh = models.CharField(max_length=50, blank=True, null=True, help_text="Khmer badge text")
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    """Customer model (no login required)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    loyalty_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        indexes = [
            models.Index(fields=['phone']),  # Already unique, but index for lookups
            models.Index(fields=['updated_at']),  # For recent customer queries
            models.Index(fields=['created_at']),  # For date-based queries
        ]
    
    def __str__(self):
        return f"{self.name} ({self.phone})"
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            # Generate unique referral code from phone number
            self.referral_code = f"MD{self.phone[-6:].upper()}"
        super().save(*args, **kwargs)


class Order(models.Model):
    """Order model"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready_for_delivery', 'Ready for Delivery'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('KHQR', 'KHQR'),
        ('ACLEDA Bank', 'ACLEDA Bank'),
        ('Wing Money', 'Wing Money'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    customer_address = models.TextField()
    customer_province = models.CharField(max_length=100)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    promo_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, null=True, blank=True)
    loyalty_points_used = models.IntegerField(default=0)
    loyalty_points_earned = models.IntegerField(default=0)
    referral_code_used = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Cash on Delivery (COD) payment tracking
    payment_received = models.BooleanField(default=False, help_text="For COD: Payment received from customer")
    payment_received_at = models.DateTimeField(null=True, blank=True, help_text="When payment was received")
    payment_received_by = models.CharField(max_length=200, blank=True, null=True, help_text="Admin/staff who confirmed payment")
    cod_delivery_notes = models.TextField(blank=True, null=True, help_text="Notes about COD delivery/payment")
    
    # Verification fields
    is_verified = models.BooleanField(default=False, help_text="Manually verified by admin")
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Verification'),
            ('verified', 'Verified'),
            ('suspicious', 'Suspicious - Needs Review'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
        help_text="Order verification status"
    )
    verification_notes = models.TextField(blank=True, null=True, help_text="Admin notes about verification")
    verified_by = models.CharField(max_length=200, blank=True, null=True, help_text="Admin who verified this order")
    verified_at = models.DateTimeField(null=True, blank=True)
    is_suspicious = models.BooleanField(default=False, help_text="Flagged as suspicious order")
    suspicious_reason = models.CharField(max_length=500, blank=True, null=True, help_text="Reason for flagging as suspicious")
    
    # Customer received tracking (for all order types)
    customer_received = models.BooleanField(default=False, help_text="Whether the customer has physically received the order")
    customer_received_at = models.DateTimeField(null=True, blank=True, help_text="When the customer received the order")
    customer_received_by = models.CharField(max_length=200, blank=True, null=True, help_text="Admin/staff who confirmed customer received")
    customer_received_notes = models.TextField(blank=True, null=True, help_text="Notes about customer receiving the order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        indexes = [
            models.Index(fields=['status', 'created_at']),  # For dashboard queries
            models.Index(fields=['customer_phone']),  # For customer order lookups
            models.Index(fields=['payment_received']),  # For COD payment queries
            models.Index(fields=['customer_received']),  # For delivery tracking
            models.Index(fields=['order_number']),  # Already unique, but index for lookups
            models.Index(fields=['created_at']),  # For date-based queries
            models.Index(fields=['status', 'customer_received']),  # Composite for dashboard filtering
        ]
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def validate_status_transition(self, new_status):
        """Validate if status transition is allowed"""
        valid_transitions = {
            'pending': ['confirmed', 'preparing', 'cancelled'],
            'confirmed': ['preparing', 'cancelled'],
            'preparing': ['ready_for_delivery', 'cancelled'],
            'ready_for_delivery': ['out_for_delivery', 'cancelled'],
            'out_for_delivery': ['delivered', 'cancelled'],
            'delivered': [],  # Final state, no transitions allowed
            'cancelled': [],  # Final state, no transitions allowed
        }
        
        current_status = self.status
        allowed_statuses = valid_transitions.get(current_status, [])
        
        if new_status not in allowed_statuses:
            raise ValidationError(
                f'Invalid status transition: Cannot change from "{current_status}" to "{new_status}". '
                f'Allowed transitions: {", ".join(allowed_statuses) if allowed_statuses else "None (final state)"}'
            )
        
        return True
    
    def check_suspicious(self):
        """Check if order is suspicious and flag it"""
        suspicious_reasons = []
        
        # Check 1: Multiple orders from same phone with different names
        if self.customer_phone:
            orders_same_phone = Order.objects.filter(customer_phone=self.customer_phone).exclude(id=self.id if self.id else None)
            unique_names = orders_same_phone.values_list('customer_name', flat=True).distinct()
            if len(unique_names) > 1:
                suspicious_reasons.append(f"Same phone used with {len(unique_names)} different names")
        
        # Check 2: Very high order value (potential fraud)
        if self.total > 1000:  # Adjust threshold as needed
            suspicious_reasons.append(f"High order value: ${self.total}")
        
        # Check 3: Multiple orders in short time
        if self.customer_phone:
            recent_orders = Order.objects.filter(
                customer_phone=self.customer_phone,
                created_at__gte=timezone.now() - timedelta(hours=1)
            ).exclude(id=self.id if self.id else None).count()
            if recent_orders >= 3:
                suspicious_reasons.append(f"{recent_orders} orders in last hour")
        
        # Check 4: Customer has no previous orders but large order
        if self.customer:
            previous_orders = Order.objects.filter(customer=self.customer).exclude(id=self.id if self.id else None).count()
            if previous_orders == 0 and self.total > 100:
                suspicious_reasons.append("First-time customer with large order")
        
        if suspicious_reasons:
            self.is_suspicious = True
            self.suspicious_reason = "; ".join(suspicious_reasons)
            self.verification_status = 'suspicious'
            return True
        return False
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate sequential order number
            # Find the last order with a valid numeric order number
            last_valid_order = None
            last_num = 0
            
            # Try to find last valid order number
            orders = Order.objects.exclude(order_number__isnull=True).exclude(order_number='').order_by('-id')
            for order in orders:
                try:
                    # Extract number from order_number (format: MD00001, MD12345, etc.)
                    order_num_str = order.order_number.replace('#', '').replace('MD', '').strip()
                    # Try to parse as integer
                    if order_num_str.isdigit():
                        last_num = int(order_num_str)
                        last_valid_order = order
                        break
                except (ValueError, AttributeError):
                    # Skip invalid order numbers, try next one
                    continue
            
            # Generate next sequential number
            if last_valid_order:
                self.order_number = f"MD{str(last_num + 1).zfill(5)}"
            else:
                # No valid orders found, start from 1
                self.order_number = "MD00001"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.product_name} x{self.quantity}"


class Promoter(models.Model):
    """Promoter model for commission tracking"""
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Commission rate as percentage (e.g., 5.00 for 5%)"
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Promoter"
        verbose_name_plural = "Promoters"
    
    def __str__(self):
        return self.name
    
    def get_total_commission(self):
        """Calculate total commission earned"""
        from decimal import Decimal
        orders = Order.objects.filter(promo_code__promoter=self, status__in=['confirmed', 'processing', 'shipped', 'delivered'])
        total = Decimal('0.00')
        for order in orders:
            commission = (order.total * self.commission_rate) / 100
            total += commission
        return total
    
    def get_total_orders(self):
        """Get total number of orders using this promoter's codes"""
        return Order.objects.filter(promo_code__promoter=self).count()
    
    def get_total_revenue(self):
        """Get total revenue from orders using this promoter's codes"""
        from decimal import Decimal
        from django.db.models import Sum
        orders = Order.objects.filter(promo_code__promoter=self, status__in=['confirmed', 'processing', 'shipped', 'delivered'])
        return orders.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')


class PromoCode(models.Model):
    """Promo code model"""
    code = models.CharField(max_length=50, unique=True)
    promoter = models.ForeignKey('Promoter', on_delete=models.SET_NULL, null=True, blank=True, related_name='promo_codes', help_text="Promoter who owns this promo code")
    description = models.CharField(max_length=200, blank=True, null=True)
    description_kh = models.CharField(max_length=200, blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=[
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    usage_limit = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Promo Code"
        verbose_name_plural = "Promo Codes"
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        """Check if promo code is valid"""
        if not self.is_active:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        if self.valid_until and timezone.now() > self.valid_until:
            return False
        if timezone.now() < self.valid_from:
            return False
        return True
    
    def calculate_discount(self, amount):
        """Calculate discount amount"""
        if not self.is_valid():
            return 0
        
        if amount < self.min_purchase:
            return 0
        
        if self.discount_type == 'percentage':
            discount = (amount * self.discount_value) / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = min(self.discount_value, amount)
        
        return discount


class Newsletter(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
    
    def __str__(self):
        return self.email


class Referral(models.Model):
    """Referral tracking model"""
    referrer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='referral_activities')
    referred_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='referral_received')
    referral_code = models.CharField(max_length=20)
    reward_points = models.IntegerField(default=0)
    is_rewarded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Referral"
        verbose_name_plural = "Referrals"
        unique_together = ['referrer', 'referred_customer']
    
    def __str__(self):
        return f"{self.referrer.name} referred {self.referred_customer.name}"


class LoyaltyPoint(models.Model):
    """Loyalty point transaction model"""
    TRANSACTION_TYPES = [
        ('earned', 'Earned'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('bonus', 'Bonus'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loyalty_transactions')
    points = models.IntegerField(validators=[MinValueValidator(1)])
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=200, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='loyalty_points')
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Loyalty Point Transaction"
        verbose_name_plural = "Loyalty Point Transactions"
    
    def __str__(self):
        return f"{self.customer.name} - {self.points} points ({self.transaction_type})"


class OrderQRCode(models.Model):
    """QR Code for KHQR payment orders"""
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='qr_code')
    qr_code_image = models.ImageField(upload_to='qr_codes/', help_text="QR code image file")
    qr_data = models.TextField(help_text="QR code data/content")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(help_text="QR code expiration time (10 minutes after creation)")
    is_used = models.BooleanField(default=False, help_text="Whether QR code has been used for payment")
    used_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when payment was confirmed")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order QR Code"
        verbose_name_plural = "Order QR Codes"
        indexes = [
            models.Index(fields=['expires_at', 'is_used']),  # For quick validity checks
            models.Index(fields=['order']),  # For order lookups
        ]
    
    def __str__(self):
        return f"QR Code for Order #{self.order.order_number}"
    
    def is_valid(self):
        """Check if QR code is still valid (not expired and not used)"""
        now = timezone.now()
        return now < self.expires_at and not self.is_used
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set expiration to 10 minutes after creation (improved from 5 minutes)
            self.expires_at = self.created_at + timedelta(minutes=10) if self.created_at else timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)


class HeroSlide(models.Model):
    """Hero carousel slide for homepage"""
    SLIDE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('url', 'External URL'),
    ]
    
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Optional title for the slide")
    subtitle = models.CharField(max_length=300, blank=True, null=True, help_text="Optional subtitle/description")
    slide_type = models.CharField(max_length=10, choices=SLIDE_TYPE_CHOICES, default='image', help_text="Type of media for this slide")
    
    # For image uploads
    image = models.ImageField(
        upload_to='hero_slides/',
        blank=True,
        null=True,
        help_text="Upload an image for this slide (if slide type is 'Image')",
        validators=[validate_image_file, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp', 'gif'])]
    )
    
    # For video uploads
    video = models.FileField(
        upload_to='hero_slides/videos/',
        blank=True,
        null=True,
        help_text="Upload a video for this slide (if slide type is 'Video')",
        validators=[validate_video_file, FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'mov'])]
    )
    
    # For external URLs (images or videos)
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="External URL for image or video (if slide type is 'URL')"
    )
    
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Show this slide in the carousel")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"
    
    def __str__(self):
        media_type = self.slide_type
        if self.title:
            return f"{self.title} ({media_type})"
        return f"Hero Slide #{self.id} ({media_type})"
    
    def get_media_url(self):
        """Get the URL for the slide media"""
        if self.slide_type == 'image' and self.image:
            return self.image.url
        elif self.slide_type == 'video' and self.video:
            return self.video.url
        elif self.slide_type == 'url' and self.external_url:
            return self.external_url
        return None
