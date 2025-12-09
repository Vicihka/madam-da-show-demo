from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (
    Product, Customer, Order, OrderItem, PromoCode, Promoter,
    Newsletter, Referral, LoyaltyPoint, OrderQRCode, HeroSlide
)


# ========== IMPORT/EXPORT RESOURCES ==========
class ProductResource(resources.ModelResource):
    """Resource for importing/exporting products with image URL support"""
    image_url = resources.Field(column_name='image_url', readonly=False)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'name_kh', 'description', 'description_kh', 'price', 'old_price', 
                 'badge', 'badge_kh', 'stock', 'is_active', 'image_url')
        import_id_fields = ['id']
        skip_unchanged = True
        report_skipped = True
        export_order = ('id', 'name', 'name_kh', 'description', 'description_kh', 'price', 'old_price',
                       'badge', 'badge_kh', 'stock', 'is_active', 'image_url')
    
    def dehydrate_image_url(self, product):
        """Export image URL if image exists"""
        if product.image:
            # Return full URL or relative path
            try:
                return product.image.url
            except:
                return str(product.image) if product.image else ''
        return ''
    
    def dehydrate_name_kh(self, product):
        """Ensure Khmer text is properly encoded"""
        return product.name_kh or ''
    
    def dehydrate_description_kh(self, product):
        """Ensure Khmer text is properly encoded"""
        return product.description_kh or ''
    
    def dehydrate_badge_kh(self, product):
        """Ensure Khmer text is properly encoded"""
        return product.badge_kh or ''
    
    def before_import_row(self, row, **kwargs):
        """Handle image URL before importing - store for later processing"""
        if 'image_url' in row:
            row['_image_url'] = row.get('image_url', '')
    
    def after_import_instance(self, instance, new, row, **kwargs):
        """Note: Image URLs need to be uploaded manually in admin panel after import"""
        # Image URLs from Excel cannot be automatically downloaded for security reasons
        # Users should upload images manually or use the image_url as reference
        pass


class PromoCodeResource(resources.ModelResource):
    """Resource for importing/exporting promo codes"""
    class Meta:
        model = PromoCode
        fields = ('code', 'description', 'description_kh', 'discount_type', 'discount_value', 
                 'min_purchase', 'max_discount', 'usage_limit', 'is_active', 
                 'valid_from', 'valid_until')
        import_id_fields = ['code']
        skip_unchanged = True
        report_skipped = True


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'price', 'old_price', 'stock', 'is_active', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at', 'badge']
    search_fields = ['id', 'name', 'name_kh', 'description']
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'name_kh', 'description', 'description_kh')
        }),
        ('Pricing', {
            'fields': ('price', 'old_price')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'badge', 'badge_kh')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_active')
        }),
    )
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    resource_class = ProductResource
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 200px; max-height: 200px; border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "No image uploaded"
    image_preview.short_description = 'Preview'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'loyalty_points', 'referral_code', 'order_count', 'created_at']
    list_filter = ['created_at', 'province']
    search_fields = ['name', 'phone', 'email', 'referral_code']
    readonly_fields = ['id', 'referral_code', 'created_at', 'updated_at']
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'phone', 'email', 'address', 'province')
        }),
        ('Loyalty & Referral', {
            'fields': ('loyalty_points', 'referral_code', 'referred_by')
        }),
    )
    
    def order_count(self, obj):
        return obj.orders.count()
    order_count.short_description = 'Orders'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'customer_phone', 'total', 'status', 'payment_status_display', 'cod_qr_code_display', 'verification_status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_received', 'verification_status', 'is_suspicious', 'created_at', 'promo_code__promoter', 'is_verified']
    search_fields = ['order_number', 'customer_name', 'customer_phone', 'customer_email', 'promo_code__code']
    readonly_fields = ['order_number', 'promoter_commission', 'created_at', 'updated_at', 'verified_at', 'payment_received_at']
    actions = ['verify_orders', 'mark_suspicious', 'mark_verified', 'reject_orders', 'confirm_cod_payment', 'mark_cod_paid']
    inlines = [OrderItemInline]
    
    change_list_template = 'admin/orders_change_list.html'
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'status', 'created_at', 'updated_at')
        }),
        ('Customer Information', {
            'fields': ('customer', 'customer_name', 'customer_phone', 'customer_email', 'customer_address', 'customer_province')
        }),
        ('Payment & Pricing', {
            'fields': ('payment_method', 'subtotal', 'shipping_fee', 'discount_amount', 'total', 'promo_code')
        }),
        ('Cash on Delivery (COD)', {
            'fields': ('payment_received', 'payment_received_at', 'payment_received_by', 'cod_delivery_notes'),
            'classes': ('collapse',),
            'description': 'For Cash on Delivery orders - confirm when payment is received'
        }),
        ('Verification', {
            'fields': ('verification_status', 'is_verified', 'is_suspicious', 'suspicious_reason', 'verification_notes', 'verified_by', 'verified_at'),
            'classes': ('collapse',)
        }),
        ('Loyalty & Referral', {
            'fields': ('loyalty_points_used', 'loyalty_points_earned', 'referral_code_used')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing order
            return self.readonly_fields + ['order_number', 'customer', 'customer_name', 'customer_phone', 
                                         'customer_email', 'customer_address', 'customer_province', 
                                         'subtotal', 'shipping_fee', 'discount_amount', 'total']
        return self.readonly_fields
    
    def promoter_commission(self, obj):
        """Calculate commission for this order"""
        if obj.promo_code and obj.promo_code.promoter and obj.status in ['confirmed', 'processing', 'shipped', 'delivered']:
            commission = (obj.total * obj.promo_code.promoter.commission_rate) / 100
            return format_html(
                '<span style="color: #28a745; font-weight: 600;">${:.2f}</span><br><small style="color: #666;">{} ({:.2f}%)</small>',
                commission,
                obj.promo_code.promoter.name,
                obj.promo_code.promoter.commission_rate
            )
        return "-"
    promoter_commission.short_description = 'Promoter Commission'
    
    def verify_orders(self, request, queryset):
        """Admin action to verify selected orders"""
        count = queryset.update(
            is_verified=True,
            verification_status='verified',
            verified_by=request.user.username,
            verified_at=timezone.now()
        )
        self.message_user(request, f'{count} order(s) marked as verified.')
    verify_orders.short_description = "Verify selected orders"
    
    def mark_suspicious(self, request, queryset):
        """Admin action to mark orders as suspicious"""
        count = queryset.update(
            is_suspicious=True,
            verification_status='suspicious'
        )
        self.message_user(request, f'{count} order(s) marked as suspicious.')
    mark_suspicious.short_description = "Mark as suspicious"
    
    def mark_verified(self, request, queryset):
        """Admin action to mark orders as verified"""
        count = queryset.update(
            is_verified=True,
            verification_status='verified',
            verified_by=request.user.username,
            verified_at=timezone.now(),
            is_suspicious=False
        )
        self.message_user(request, f'{count} order(s) marked as verified.')
    mark_verified.short_description = "Mark as verified"
    
    def reject_orders(self, request, queryset):
        """Admin action to reject orders"""
        count = queryset.update(
            verification_status='rejected',
            is_suspicious=True
        )
        self.message_user(request, f'{count} order(s) rejected.')
    reject_orders.short_description = "Reject orders"
    
    def payment_status_display(self, obj):
        """Display payment status for COD orders"""
        if obj.payment_method == 'Cash on Delivery':
            if obj.payment_received:
                return format_html('<span style="color: #28a745; font-weight: 600;">✅ Paid</span>')
            else:
                return format_html('<span style="color: #dc3545; font-weight: 600;">⏳ Pending</span>')
        else:
            return format_html('<span style="color: #6c757d;">Online</span>')
    payment_status_display.short_description = 'Payment Status'
    
    def cod_qr_code_display(self, obj):
        """Display QR code link for COD orders"""
        if obj.payment_method == 'Cash on Delivery' and not obj.payment_received:
            qr_url = reverse('cod_qr', args=[obj.order_number])
            print_url = reverse('cod_print', args=[obj.order_number])
            return format_html(
                '<a href="{}" target="_blank" style="margin-right: 10px;">📱 View QR</a>'
                '<a href="{}" target="_blank" style="background: #28a745; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;">🖨️ Print</a>',
                qr_url,
                print_url
            )
        return "-"
    cod_qr_code_display.short_description = 'QR Code'
    
    def confirm_cod_payment(self, request, queryset):
        """Admin action to confirm COD payment received"""
        from django.utils import timezone
        cod_orders = queryset.filter(payment_method='Cash on Delivery', payment_received=False)
        count = cod_orders.update(
            payment_received=True,
            payment_received_at=timezone.now(),
            payment_received_by=request.user.username,
            status='confirmed'  # Move to confirmed when payment received
        )
        self.message_user(request, f'{count} COD order(s) marked as payment received.')
    confirm_cod_payment.short_description = "Confirm COD Payment Received"
    
    def mark_cod_paid(self, request, queryset):
        """Admin action to mark COD orders as paid"""
        from django.utils import timezone
        cod_orders = queryset.filter(payment_method='Cash on Delivery')
        count = cod_orders.update(
            payment_received=True,
            payment_received_at=timezone.now(),
            payment_received_by=request.user.username
        )
        self.message_user(request, f'{count} COD order(s) marked as paid.')
    mark_cod_paid.short_description = "Mark COD as Paid"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales-report/', self.admin_site.admin_view(self.sales_report_view), name='app_order_sales_report'),
            path('commission-report/', self.admin_site.admin_view(self.commission_report_view), name='app_order_commission_report'),
        ]
        return custom_urls + urls
    
    def sales_report_view(self, request):
        """Sales report view"""
        # Get date range from request
        today = timezone.now().date()
        start_date = request.GET.get('start_date', (today - timedelta(days=30)).strftime('%Y-%m-%d'))
        end_date = request.GET.get('end_date', today.strftime('%Y-%m-%d'))
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        except:
            start = today - timedelta(days=30)
            end = today
        
        # Filter orders by date range
        orders = Order.objects.filter(created_at__date__gte=start, created_at__date__lte=end)
        
        # Calculate statistics
        total_orders = orders.count()
        total_revenue = orders.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
        total_subtotal = orders.aggregate(Sum('subtotal'))['subtotal__sum'] or Decimal('0.00')
        total_discount = orders.aggregate(Sum('discount_amount'))['discount_amount__sum'] or Decimal('0.00')
        total_shipping = orders.aggregate(Sum('shipping_fee'))['shipping_fee__sum'] or Decimal('0.00')
        average_order_value = orders.aggregate(Avg('total'))['total__avg'] or Decimal('0.00')
        
        # Orders by status
        orders_by_status = orders.values('status').annotate(
            count=Count('id'),
            total=Sum('total')
        ).order_by('-count')
        
        # Orders by payment method
        orders_by_payment = orders.values('payment_method').annotate(
            count=Count('id'),
            total=Sum('total')
        ).order_by('-count')
        
        # Top products
        top_products = OrderItem.objects.filter(
            order__created_at__date__gte=start,
            order__created_at__date__lte=end
        ).values('product_name').annotate(
            quantity=Sum('quantity'),
            revenue=Sum('subtotal')
        ).order_by('-revenue')[:10]
        
        # Daily sales (last 30 days)
        daily_sales = []
        current_date = start
        while current_date <= end:
            day_orders = orders.filter(created_at__date=current_date)
            day_total = day_orders.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
            day_count = day_orders.count()
            daily_sales.append({
                'date': current_date,
                'total': day_total,
                'count': day_count
            })
            current_date += timedelta(days=1)
        
        # All-time statistics
        all_time_orders = Order.objects.all()
        all_time_revenue = all_time_orders.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
        all_time_count = all_time_orders.count()
        
        context = {
            'title': 'Sales Report',
            'start_date': start,
            'end_date': end,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_subtotal': total_subtotal,
            'total_discount': total_discount,
            'total_shipping': total_shipping,
            'average_order_value': average_order_value,
            'orders_by_status': orders_by_status,
            'orders_by_payment': orders_by_payment,
            'top_products': top_products,
            'daily_sales': daily_sales,
            'all_time_revenue': all_time_revenue,
            'all_time_count': all_time_count,
        }
        
        return render(request, 'admin/sales_report.html', context)
    
    def commission_report_view(self, request):
        """Commission report view for promoters"""
        # Get date range from request
        today = timezone.now().date()
        start_date = request.GET.get('start_date', (today - timedelta(days=30)).strftime('%Y-%m-%d'))
        end_date = request.GET.get('end_date', today.strftime('%Y-%m-%d'))
        promoter_id = request.GET.get('promoter', '')
        
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
        except:
            start = today - timedelta(days=30)
            end = today
        
        # Get all promoters
        from .models import Promoter
        promoters = Promoter.objects.all()
        if promoter_id:
            promoters = promoters.filter(id=promoter_id)
        
        # Calculate commission for each promoter
        promoter_data = []
        for promoter in promoters:
            orders = Order.objects.filter(
                promo_code__promoter=promoter,
                created_at__date__gte=start,
                created_at__date__lte=end,
                status__in=['confirmed', 'processing', 'shipped', 'delivered']
            )
            
            total_orders = orders.count()
            total_revenue = orders.aggregate(Sum('total'))['total__sum'] or Decimal('0.00')
            total_commission = Decimal('0.00')
            
            for order in orders:
                commission = (order.total * promoter.commission_rate) / 100
                total_commission += commission
            
            # Get promo codes for this promoter
            promo_codes = promoter.promo_codes.all()
            codes_used = {}
            for code in promo_codes:
                code_orders = orders.filter(promo_code=code)
                codes_used[code.code] = {
                    'count': code_orders.count(),
                    'revenue': code_orders.aggregate(Sum('total'))['total__sum'] or Decimal('0.00'),
                    'commission': sum([(o.total * promoter.commission_rate) / 100 for o in code_orders])
                }
            
            promoter_data.append({
                'promoter': promoter,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'total_commission': total_commission,
                'codes_used': codes_used
            })
        
        # Total commission across all promoters
        total_all_commission = sum([p['total_commission'] for p in promoter_data])
        total_all_revenue = sum([p['total_revenue'] for p in promoter_data])
        
        context = {
            'title': 'Promoter Commission Report',
            'start_date': start,
            'end_date': end,
            'promoter_id': promoter_id,
            'promoters': Promoter.objects.all(),
            'promoter_data': promoter_data,
            'total_all_commission': total_all_commission,
            'total_all_revenue': total_all_revenue,
        }
        
        return render(request, 'admin/commission_report.html', context)


@admin.register(Promoter)
class PromoterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'commission_rate', 'total_orders', 'total_revenue', 'total_commission', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['total_orders', 'total_revenue', 'total_commission', 'created_at', 'updated_at']
    fieldsets = (
        ('Promoter Information', {
            'fields': ('name', 'phone', 'email', 'is_active')
        }),
        ('Commission Settings', {
            'fields': ('commission_rate',)
        }),
        ('Statistics', {
            'fields': ('total_orders', 'total_revenue', 'total_commission'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )
    
    def total_orders(self, obj):
        return obj.get_total_orders()
    total_orders.short_description = 'Total Orders'
    
    def total_revenue(self, obj):
        return f"${obj.get_total_revenue():.2f}"
    total_revenue.short_description = 'Total Revenue'
    
    def total_commission(self, obj):
        return f"${obj.get_total_commission():.2f}"
    total_commission.short_description = 'Total Commission'


@admin.register(PromoCode)
class PromoCodeAdmin(ImportExportModelAdmin):
    list_display = ['code', 'promoter', 'discount_type', 'discount_value', 'is_active', 'used_count', 'usage_limit', 'valid_until']
    list_filter = ['is_active', 'discount_type', 'promoter', 'valid_from', 'valid_until']
    search_fields = ['code', 'description', 'promoter__name']
    readonly_fields = ['used_count', 'created_at', 'updated_at']
    resource_class = PromoCodeResource
    fieldsets = (
        ('Code Information', {
            'fields': ('code', 'promoter', 'description', 'description_kh', 'is_active')
        }),
        ('Discount Settings', {
            'fields': ('discount_type', 'discount_value', 'min_purchase', 'max_discount')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'used_count', 'valid_from', 'valid_until')
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'phone', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'name', 'phone']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['referrer', 'referred_customer', 'referral_code', 'reward_points', 'is_rewarded', 'created_at']
    list_filter = ['is_rewarded', 'created_at']
    search_fields = ['referrer__name', 'referred_customer__name', 'referral_code']
    readonly_fields = ['created_at']


@admin.register(LoyaltyPoint)
class LoyaltyPointAdmin(admin.ModelAdmin):
    list_display = ['customer', 'points', 'transaction_type', 'description', 'order', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['customer__name', 'customer__phone', 'description']
    readonly_fields = ['created_at']
    
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields


@admin.register(OrderQRCode)
class OrderQRCodeAdmin(admin.ModelAdmin):
    list_display = ['order', 'is_valid', 'is_used', 'created_at', 'expires_at', 'used_at']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['order__order_number', 'qr_data']
    readonly_fields = ['order', 'qr_code_image', 'qr_data', 'created_at', 'expires_at', 'is_used', 'used_at']
    
    def is_valid(self, obj):
        if obj:
            return obj.is_valid()
        return False
    is_valid.boolean = True
    is_valid.short_description = 'Valid'


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'slide_type', 'order', 'is_active', 'media_preview', 'created_at']
    list_filter = ['slide_type', 'is_active', 'created_at']
    search_fields = ['title', 'subtitle']
    list_editable = ['order', 'is_active']
    readonly_fields = ['media_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'slide_type', 'order', 'is_active')
        }),
        ('Media Content', {
            'fields': ('image', 'video', 'external_url', 'media_preview'),
            'description': 'Upload image/video OR provide external URL based on slide type'
        }),
    )
    
    def media_preview(self, obj):
        """Show preview of the slide media"""
        if obj.slide_type == 'image' and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px; object-fit: cover;" />',
                obj.image.url
            )
        elif obj.slide_type == 'video' and obj.video:
            return format_html(
                '<video src="{}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" controls></video>',
                obj.video.url
            )
        elif obj.slide_type == 'url' and obj.external_url:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.external_url, obj.external_url
            )
        return "No media uploaded"
    media_preview.short_description = 'Preview'
