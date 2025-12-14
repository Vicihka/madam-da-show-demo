"""
CRITICAL SCALABILITY FIXES FOR 1000+ CUSTOMERS
==============================================

Apply these fixes to make your website ready for 1000+ concurrent customers.

Priority: CRITICAL - Apply before production launch
"""

# ============================================================================
# FIX 1: Add Pagination to Product Listings (app/views.py)
# ============================================================================

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def shop_view(request):
    """Shop/homepage view - WITH PAGINATION"""
    products = Product.objects.filter(is_active=True).order_by('id')
    
    # Add pagination - 20 products per page
    paginator = Paginator(products, 20)
    page = request.GET.get('page', 1)
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    
    context = {
        'products': products,
        'hero_slides': hero_slides,
    }
    return render(request, 'app/index.html', context)


# ============================================================================
# FIX 2: Optimize Customer Lookup (app/views.py)
# ============================================================================

def customer_lookup(request):
    """API endpoint to lookup customer by phone number - OPTIMIZED"""
    try:
        phone = request.GET.get('phone', '').strip()
        
        if not phone:
            return JsonResponse({
                'success': False,
                'message': 'Phone number is required'
            }, status=400)
        
        # Normalize phone number (remove spaces, dashes, etc.)
        normalized_phone = ''.join(filter(str.isdigit, phone))
        
        if not normalized_phone:
            return JsonResponse({
                'success': False,
                'message': 'Invalid phone number format'
            }, status=400)
        
        # Try exact match first (uses index, very fast)
        try:
            customer = Customer.objects.get(phone=normalized_phone)
        except Customer.DoesNotExist:
            # Try with common prefixes (e.g., 0, +855)
            variations = [
                normalized_phone,
                f"0{normalized_phone}",
                f"+855{normalized_phone}",
                normalized_phone[-9:],  # Last 9 digits
            ]
            
            customer = None
            for phone_variant in variations:
                try:
                    customer = Customer.objects.get(phone=phone_variant)
                    break
                except Customer.DoesNotExist:
                    continue
        
        # If still not found, try to find from recent orders (limit to last 10)
        if not customer:
            try:
                order = Order.objects.filter(
                    customer_phone=normalized_phone  # Exact match, uses index
                ).order_by('-created_at').first()
                
                if order:
                    return JsonResponse({
                        'success': True,
                        'customer': {
                            'name': order.customer_name,
                            'phone': order.customer_phone,
                            'address': order.customer_address or '',
                            'province': order.customer_province or ''
                        }
                    })
            except Exception as e:
                logger.warning(f"Error looking up customer from orders: {str(e)}")
        
        if customer:
            return JsonResponse({
                'success': True,
                'customer': {
                    'name': customer.name,
                    'phone': customer.phone,
                    'address': customer.address or '',
                    'province': customer.province or ''
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Customer not found'
            })
            
    except Exception as e:
        logger.error(f"Error in customer_lookup: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while looking up customer'
        }, status=500)


# ============================================================================
# FIX 3: Add Query Limits to Employee Dashboard (app/employee_views.py)
# ============================================================================

def employee_dashboard(request):
    """Main employee dashboard - WITH QUERY LIMITS"""
    
    # Limit each query to prevent loading too many orders
    MAX_ORDERS_PER_STATUS = 100
    
    orders_to_prepare = Order.objects.filter(
        status__in=['pending', 'confirmed']
    ).exclude(status='cancelled').exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product'))
    ).order_by('-created_at')[:MAX_ORDERS_PER_STATUS]  # ✅ ADD LIMIT
    
    orders_preparing = Order.objects.filter(
        status='preparing'
    ).exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product'))
    ).order_by('-created_at')[:MAX_ORDERS_PER_STATUS]  # ✅ ADD LIMIT
    
    orders_ready = Order.objects.filter(
        status='ready_for_delivery'
    ).exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related('items').order_by('-created_at')[:MAX_ORDERS_PER_STATUS]  # ✅ ADD LIMIT
    
    orders_out = Order.objects.filter(
        status='out_for_delivery'
    ).exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related('items').order_by('-created_at')[:MAX_ORDERS_PER_STATUS]  # ✅ ADD LIMIT
    
    # Already limited to 50, keep it
    from datetime import timedelta
    seven_days_ago = timezone.now() - timedelta(days=7)
    orders_delivered_today = Order.objects.filter(
        status='delivered',
        updated_at__gte=seven_days_ago
    ).select_related(
        'customer', 'promo_code'
    ).prefetch_related('items').order_by('-updated_at')[:50]
    
    context = {
        'orders_to_prepare': orders_to_prepare,
        'orders_preparing': orders_preparing,
        'orders_ready': orders_ready,
        'orders_out': orders_out,
        'orders_delivered_today': orders_delivered_today,
        'total_to_prepare': orders_to_prepare.count(),
        'total_preparing': orders_preparing.count(),
        'total_ready': orders_ready.count(),
        'total_out': orders_out.count(),
    }
    
    return render(request, 'app/employee_dashboard.html', context)


# ============================================================================
# FIX 4: Add Caching for Product Listings (app/views.py)
# ============================================================================

from django.core.cache import cache
from django.views.decorators.cache import cache_page

# Option 1: Cache the entire view (simplest)
@cache_page(300)  # Cache for 5 minutes
def shop_view(request):
    """Shop/homepage view - WITH CACHING"""
    products = Product.objects.filter(is_active=True).order_by('id')
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    
    context = {
        'products': products,
        'hero_slides': hero_slides,
    }
    return render(request, 'app/index.html', context)


# Option 2: Cache only the data (more control)
def shop_view(request):
    """Shop/homepage view - WITH SELECTIVE CACHING"""
    # Cache products for 5 minutes
    cache_key_products = 'active_products'
    products = cache.get(cache_key_products)
    
    if not products:
        products = list(Product.objects.filter(is_active=True).order_by('id'))
        cache.set(cache_key_products, products, 300)  # 5 minutes
    
    # Cache hero slides for 10 minutes (change less frequently)
    cache_key_slides = 'active_hero_slides'
    hero_slides = cache.get(cache_key_slides)
    
    if not hero_slides:
        hero_slides = list(HeroSlide.objects.filter(is_active=True).order_by('order'))
        cache.set(cache_key_slides, hero_slides, 600)  # 10 minutes
    
    context = {
        'products': products,
        'hero_slides': hero_slides,
    }
    return render(request, 'app/index.html', context)


# ============================================================================
# FIX 5: Add WebSocket Connection Limits (app/consumers.py)
# ============================================================================

class OrderConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for order updates - WITH CONNECTION LIMITS"""
    
    MAX_CONNECTIONS = 100  # Maximum concurrent connections
    current_connections = 0  # Track current connections (use Redis in production)
    
    async def connect(self):
        """Called when WebSocket connection is established"""
        # Check connection limit
        # In production, use Redis to track connections across workers
        if OrderConsumer.current_connections >= self.MAX_CONNECTIONS:
            await self.close(code=4001)  # Close with custom code
            return
        
        # Join the 'orders_updates' group
        self.group_name = 'orders_updates'
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        OrderConsumer.current_connections += 1
        await self.accept()
        print(f"WebSocket connected: {self.channel_name} (Total: {OrderConsumer.current_connections})")
    
    async def disconnect(self, close_code):
        """Called when WebSocket connection is closed"""
        # Leave the 'orders_updates' group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        OrderConsumer.current_connections = max(0, OrderConsumer.current_connections - 1)
        print(f"WebSocket disconnected: {self.channel_name} (Total: {OrderConsumer.current_connections})")


# ============================================================================
# FIX 6: Update settings.py for PostgreSQL Connection Pooling
# ============================================================================

# In project/settings.py, update DATABASES configuration:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db_name,
        'USER': db_user,
        'PASSWORD': db_password,
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 10,
            # Connection pool settings (handled by psycopg2)
        },
        'CONN_MAX_AGE': 600,  # ✅ Already set - keep connections for 10 minutes
        'ATOMIC_REQUESTS': False,  # Don't wrap each request in transaction
    }
}

# Also configure PostgreSQL max_connections:
# In PostgreSQL config (postgresql.conf):
# max_connections = 200  # Adjust based on your server capacity


# ============================================================================
# FIX 7: Ensure Rate Limiting Works in Production
# ============================================================================

# In project/settings.py, ensure:
DEBUG = False  # ✅ CRITICAL: Must be False in production

# Rate limiting will work automatically if:
# 1. DEBUG = False
# 2. Redis is running
# 3. django_ratelimit is installed (already in requirements.txt)

# Test rate limiting:
# In production, make 30 requests quickly to an endpoint with @apply_rate_limit('20/m')
# Should get 429 Too Many Requests after 20 requests


# ============================================================================
# FIX 8: Add Database Query Logging (Optional, for debugging)
# ============================================================================

# In project/settings.py, add to LOGGING:

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',  # Log all SQL queries
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# ⚠️ Only enable in development! Disable in production for performance.


# ============================================================================
# SUMMARY: Files to Update
# ============================================================================

"""
Files to modify:

1. app/views.py
   - Add pagination to shop_view()
   - Optimize customer_lookup() (remove icontains)
   - Add caching to shop_view()

2. app/employee_views.py
   - Add query limits to employee_dashboard()

3. app/consumers.py
   - Add connection limits to OrderConsumer

4. project/settings.py
   - Ensure CONN_MAX_AGE is set
   - Ensure DEBUG=False in production
   - Add query logging (optional)

5. PostgreSQL Configuration
   - Set max_connections = 200
   - Restart PostgreSQL

6. Environment Variables (.env)
   - DEBUG=False
   - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
   - REDIS_URL
"""





