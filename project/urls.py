"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.views.generic import RedirectView
from app import views
from app import employee_views
import os
from pathlib import Path

# Admin URLs (not in i18n_patterns) - Use custom URL for security
admin_url = os.environ.get('ADMIN_URL', 'admin/')
if not admin_url.endswith('/'):
    admin_url += '/'
urlpatterns = [
    path(admin_url, admin.site.urls),  # Admin panel
    path('i18n/', include('django.conf.urls.i18n')),
    # Health check endpoint (for monitoring and load balancers)
    path('health/', views.health_check, name='health_check'),
    path('api/health/', views.health_check, name='api_health_check'),
    # Silence Chrome DevTools well-known file requests
    path('.well-known/appspecific/com.chrome.devtools.json', lambda r: HttpResponse('{}', content_type='application/json')),
    # Favicon - browsers automatically request /favicon.ico
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.png', permanent=True)),
]

# Multi-language URL patterns
urlpatterns += i18n_patterns(
    path('', views.shop_view, name='shop'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/success/', views.order_success_view, name='order_success'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('contact/', views.contact_view, name='contact'),
    path('shipping-policy/', views.shipping_policy_view, name='shipping_policy'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('api/newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('api/customer/lookup/', views.customer_lookup, name='customer_lookup'),
    path('api/promo/validate/', views.validate_promo_code, name='validate_promo_code'),
    path('api/referral/check/', views.check_referral_code, name='check_referral_code'),
    path('api/loyalty/calculate/', views.calculate_loyalty_points, name='calculate_loyalty_points'),
    path('api/khqr/create/', views.create_khqr, name='create_khqr'),
    path('api/khqr/check/', views.check_payment, name='check_payment'),
    path('api/order/create-on-payment/', views.create_order_on_payment, name='create_order_on_payment'),
    # COD (Cash on Delivery) automation
    path('cod/confirm/', views.cod_confirmation_view, name='cod_confirm'),
    path('cod/confirm/<str:order_number>/', views.cod_confirmation_view, name='cod_confirm_order'),
    path('cod/qr/<str:order_number>/', views.cod_qr_view, name='cod_qr'),
    path('cod/print/<str:order_number>/', views.cod_print_view, name='cod_print'),
    path('api/cod/confirm/', views.cod_confirm_api, name='cod_confirm_api'),
    
    # Order Tracking
    path('track-order/', views.track_order_view, name='track_order'),
    path('api/order/track/', views.track_order_api, name='track_order_api'),
    
    # Employee Authentication
    path('employee/login/', employee_views.employee_login, name='employee_login'),
    path('employee/logout/', employee_views.employee_logout, name='employee_logout'),
    
    # Employee Dashboard
    path('employee/', employee_views.employee_dashboard, name='employee_dashboard'),
    path('employee/api/', employee_views.employee_dashboard_api, name='employee_dashboard_api'),
    path('employee/order/<str:order_number>/', employee_views.employee_order_detail, name='employee_order_detail'),
    path('employee/order/<str:order_number>/print/', employee_views.employee_print_qr, name='employee_print_qr'),
    path('api/employee/order/<str:order_number>/status/', employee_views.employee_update_status, name='employee_update_status'),
    path('api/employee/order/<str:order_number>/confirm-payment/', employee_views.employee_confirm_payment, name='employee_confirm_payment'),
    
    # Telegram Bot Webhook
    path('api/telegram/webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('api/telegram/set-webhook/', views.set_telegram_webhook, name='set_telegram_webhook'),
    prefix_default_language=False,
)

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
