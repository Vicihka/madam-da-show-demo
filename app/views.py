from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.utils.translation import get_language, activate
from django.utils import timezone
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.conf import settings
import requests
import json
import logging
import os
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from urllib.parse import unquote

from project.settings import BAKONG_API_BASE, BAKONG_ID, BAKONG_MERCHANT_NAME
from .models import Product, Customer, Order, OrderItem, PromoCode, Newsletter, Referral, LoyaltyPoint, OrderQRCode, HeroSlide
from .telegram_webhook import telegram_webhook, set_telegram_webhook

logger = logging.getLogger(__name__)

# Rate limiting decorator (simple version for development)
def apply_rate_limit(rate, method='GET'):
    """Simple rate limiting decorator"""
    def decorator(func):
        return func
    return decorator


# Telegram notification function
def send_telegram_notification(order):
    """Send order notification to Telegram with interactive buttons"""
    try:
        from .telegram_bot import send_new_order_notification
        
        # Use the new interactive notification system
        send_new_order_notification(order)
        
        logger.info(f"Sent interactive Telegram notification for order {order.order_number}")
        return True
    except Exception as e:
        logger.error(f"Error sending Telegram notification: {str(e)}", exc_info=True)
        
        # Fallback to simple notification
        try:
            bot_token = settings.TELEGRAM_BOT_TOKEN
            chat_id = settings.TELEGRAM_CHAT_ID
            
            if not bot_token or not chat_id:
                return False
            
            message = f"""🛒 NEW ORDER RECEIVED!

📦 Order: {order.order_number}
👤 Customer: {order.customer_name}
📱 Phone: {order.customer_phone}
💵 Total: ${order.total}
💳 Payment: {order.payment_method}
"""
            
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, json={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }, timeout=10)
            return True
        except:
            return False
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                logger.info(f"✅ Telegram notification sent successfully for order {order.order_number}")
                return True
            else:
                logger.error(f"❌ Telegram API returned error: {result.get('description', 'Unknown error')}")
                return False
        else:
            logger.error(f"❌ Failed to send Telegram notification. Status: {response.status_code}, Response: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error sending Telegram notification: {str(e)}", exc_info=True)
        return False


@ensure_csrf_cookie
def shop_view(request):
    """Shop/homepage view"""
    products = Product.objects.filter(is_active=True).order_by('id')
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')
    
    context = {
        'products': products,
        'hero_slides': hero_slides,
    }
    return render(request, 'app/index.html', context)


@ensure_csrf_cookie
def checkout_view(request):
    """Checkout page view"""
    return render(request, 'app/checkout.html')


def order_success_view(request):
    """Order success page view"""
    # Get order data from query parameters
    order_number = request.GET.get('order', '00123')
    name = request.GET.get('name', '')
    phone = request.GET.get('phone', '')
    address = request.GET.get('address', '')
    province = request.GET.get('province', '')
    payment_method = request.GET.get('payment', 'KHQR')
    total = request.GET.get('total', '0.00')
    subtotal_param = request.GET.get('subtotal', '')
    discount_param = request.GET.get('discount', '0.00')
    qr_url = request.GET.get('qr_url', '')
    
    # Get order items from query parameters (JSON encoded)
    items_json = request.GET.get('items', '[]')
    try:
        items = json.loads(unquote(items_json))
        if subtotal_param:
            subtotal = float(subtotal_param)
        else:
            subtotal = sum(float(item.get('price', 0)) * int(item.get('qty', 0)) for item in items)
    except:
        items = []
        subtotal = float(total) if not subtotal_param else float(subtotal_param)
    
    discount_amount = float(discount_param) if discount_param else 0.0
    
    # Format current date and time
    now = timezone.now()
    order_date = now.strftime('%B %d, %Y - %I:%M %p')
    
    # Try to get or create order in database
    order = None
    qr_code_obj = None
    try:
        # Check if order already exists (might have been created when payment was confirmed)
        # Validate order number format - if it contains non-digit characters after MD, it's invalid
        if order_number and order_number.startswith('MD'):
            # Extract numeric part
            numeric_part = order_number.replace('MD', '').replace('#', '').strip()
            # If numeric part is not all digits, try to find the order by the provided number first
            if not numeric_part.isdigit():
                # Invalid format like "MD00NEW" - try to find order by exact match first
                try:
                    order = Order.objects.get(order_number=order_number)
                    logger.info(f"Order {order_number} found by exact match")
                except Order.DoesNotExist:
                    # If not found, this is an invalid order number
                    logger.warning(f"Invalid order number format: {order_number}. Order may not exist.")
                    order = None
            else:
                # Valid format - format it properly
                order_number_formatted = f"MD{numeric_part.zfill(5)}"
                try:
                    order = Order.objects.get(order_number=order_number_formatted)
                    logger.info(f"Order {order_number_formatted} already exists, skipping creation in order_success_view")
                except Order.DoesNotExist:
                    # Try exact match as fallback
                    try:
                        order = Order.objects.get(order_number=order_number)
                        logger.info(f"Order {order_number} found by exact match (fallback)")
                    except Order.DoesNotExist:
                        order = None
        else:
            # Format order number if it doesn't start with MD
            order_number_formatted = f"MD{order_number.zfill(5)}" if order_number and order_number.isdigit() else order_number
            try:
                order = Order.objects.get(order_number=order_number_formatted)
                logger.info(f"Order {order_number_formatted} already exists")
            except Order.DoesNotExist:
                # Try exact match
                try:
                    order = Order.objects.get(order_number=order_number)
                    logger.info(f"Order {order_number} found by exact match")
                except Order.DoesNotExist:
                    order = None
        
        # If order not found and we have valid data, create it
        if not order and name and phone and address:
            # This path should ideally not be taken if create_order_on_payment is called
            logger.warning(f"Order not found, creating in order_success_view. This might indicate a missed payment confirmation.")
            # Get or create customer
            customer, _ = Customer.objects.get_or_create(
                phone=phone,
                defaults={'name': name, 'address': address, 'province': province}
            )
            
            # Don't set order_number - let the model generate it sequentially
            # Create order without order_number to trigger auto-generation
            order = Order(
                customer=customer,
                customer_name=name,
                customer_phone=phone,
                customer_address=address,
                customer_province=province,
                subtotal=Decimal(str(subtotal)),
                shipping_fee=Decimal('0.00'),
                discount_amount=Decimal(str(discount_amount)),
                total=Decimal(str(total)),
                payment_method=payment_method,
                status='pending',
                customer_received=False,
                payment_received=False
            )
            # Save to trigger order_number generation
            order.save()
            
            # Create order items
            for item in items:
                product_id = item.get('id')
                product_name = item.get('name', 'Unknown Product')
                product_price = Decimal(str(item.get('price', 0)))
                quantity = int(item.get('qty', 1))
                
                product = None
                if product_id:
                    try:
                        product = Product.objects.get(id=product_id)
                    except Product.DoesNotExist:
                        pass
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product_name,
                    product_price=product_price,
                    quantity=quantity,
                    subtotal=product_price * quantity
                )
            
            # Send Telegram notification only if order was just created in this view
            order.refresh_from_db()
            try:
                logger.info(f"Order created in order_success_view: {order.order_number}, sending Telegram notification...")
                send_telegram_notification(order)
            except Exception as e:
                logger.error(f"Failed to send Telegram notification from order_success_view: {str(e)}", exc_info=True)
        
        # If KHQR payment and QR URL provided, create QR code
        if payment_method == 'KHQR' and qr_url and order:
            try:
                # Check if QR code already exists for this order
                qr_code_obj = OrderQRCode.objects.filter(order=order).first()
                if not qr_code_obj:
                    # Download QR code image from URL
                    qr_response = requests.get(qr_url, timeout=10)
                    if qr_response.status_code == 200:
                        # Generate QR code image using qrcode library
                        qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4,
                        )
                        qr.add_data(qr_url)
                        qr.make(fit=True)
                        
                        # Create image
                        img = qr.make_image(fill_color="black", back_color="white")
                        
                        # Save to BytesIO
                        img_io = BytesIO()
                        img.save(img_io, format='PNG')
                        img_io.seek(0)
                        
                        # Create OrderQRCode
                        qr_code_obj = OrderQRCode.objects.create(
                            order=order,
                            qr_data=qr_url,
                            expires_at=now + timedelta(minutes=5)
                        )
                        qr_code_obj.qr_code_image.save(
                            f'qr_{order.order_number}.png',
                            ContentFile(img_io.read()),
                            save=True
                        )
                else:
                    logger.info(f"QR code for order {order.order_number} already exists.")
            except Exception as e:
                logger.error(f"Error creating QR code: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error saving order in order_success_view: {str(e)}")
    
    # Get the actual order number - prefer from order object, fallback to formatted query param
    # If order_number contains "NEW" or is invalid, use the order's actual number
    if order:
        display_order_number = order.order_number
    elif order_number and ('NEW' in str(order_number).upper() or not order_number.startswith('MD') or len(order_number.replace('MD', '').replace('#', '').strip()) < 3):
        # Invalid order number format - try to find by other means or use placeholder
        display_order_number = order_number  # Will show as-is, but should be fixed by proper order creation
    else:
        display_order_number = order_number if order_number else 'N/A'
    
    context = {
        'order': order,
        'order_number': display_order_number,
        'name': name,
        'phone': phone,
        'address': address,
        'province': province,
        'payment_method': payment_method,
        'total': total,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'items': items,
        'order_date': order.created_at.strftime('%B %d, %Y - %I:%M %p') if order else order_date,
        'qr_code_image_url': qr_code_obj.qr_code_image.url if qr_code_obj and qr_code_obj.qr_code_image else None,
        'qr_code_expires_at': qr_code_obj.expires_at.isoformat() if qr_code_obj else None,
    }
    return render(request, 'app/order_success.html', context)


def about_us_view(request):
    """About us page view"""
    return render(request, 'app/about_us.html')


def contact_view(request):
    """Contact page view"""
    return render(request, 'app/contact.html')


def shipping_policy_view(request):
    """Shipping policy page view"""
    return render(request, 'app/shipping_policy.html')


def privacy_policy_view(request):
    """Privacy policy page view"""
    return render(request, 'app/privacy_policy.html')


@apply_rate_limit('20/m', 'POST')
@require_http_methods(["POST"])
@csrf_exempt
def newsletter_subscribe(request):
    """Newsletter subscription endpoint"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email is required'
            }, status=400)
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid email address'
            }, status=400)
        
        # Get or create newsletter subscription
        newsletter, created = Newsletter.objects.get_or_create(email=email)
        
        if created:
            return JsonResponse({
                'success': True,
                'message': 'Successfully subscribed to newsletter!'
            })
        else:
            return JsonResponse({
                'success': True,
                'message': 'You are already subscribed!'
            })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in newsletter_subscribe: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)


@apply_rate_limit('30/m', 'POST')
@require_http_methods(["POST"])
@csrf_exempt
def validate_promo_code(request):
    """Validate promo code and calculate discount"""
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
        amount = Decimal(str(data.get('amount', 0)))
        
        if not code:
            return JsonResponse({
                'success': False,
                'message': 'Promo code is required'
            }, status=400)
        
        try:
            promo = PromoCode.objects.get(code=code, is_active=True)
            
            # Check if promo code is valid
            now = timezone.now()
            if promo.valid_from and promo.valid_from > now:
                return JsonResponse({
                    'success': False,
                    'message': 'Promo code is not yet valid'
                }, status=400)
            
            if promo.valid_until and promo.valid_until < now:
                return JsonResponse({
                    'success': False,
                    'message': 'Promo code has expired'
                }, status=400)
            
            # Check minimum amount
            if promo.minimum_amount and amount < promo.minimum_amount:
                return JsonResponse({
                    'success': False,
                    'message': f'Minimum order amount is ${promo.minimum_amount}'
                }, status=400)
            
            # Calculate discount
            if promo.discount_type == 'percentage':
                discount = (amount * promo.discount_value) / 100
                if promo.maximum_discount:
                    discount = min(discount, promo.maximum_discount)
            else:
                discount = promo.discount_value
            
            discount = min(discount, amount)  # Don't discount more than total
            
            return JsonResponse({
                'success': True,
                'code': promo.code,
                'discount_amount': float(discount),
                'discount_type': promo.discount_type,
                'discount_value': float(promo.discount_value),
                'message': f'Discount applied: ${discount:.2f}'
            })
        
        except PromoCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid promo code'
            }, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in validate_promo_code: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)


@apply_rate_limit('30/m', 'POST')
@require_http_methods(["POST"])
@csrf_exempt
def check_referral_code(request):
    """Check referral code validity"""
    try:
        data = json.loads(request.body)
        code = data.get('code', '').strip().upper()
        
        if not code:
            return JsonResponse({
                'success': False,
                'message': 'Referral code is required'
            }, status=400)
        
        try:
            customer = Customer.objects.get(referral_code=code)
            return JsonResponse({
                'success': True,
                'message': 'Valid referral code'
            })
        except Customer.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid referral code'
            }, status=404)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in check_referral_code: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)


@apply_rate_limit('30/m', 'POST')
@require_http_methods(["POST"])
@csrf_exempt
def calculate_loyalty_points(request):
    """Calculate loyalty points for an order"""
    try:
        data = json.loads(request.body)
        amount = Decimal(str(data.get('amount', 0)))
        points_used = int(data.get('points_used', 0))
        
        # Calculate points earned (1 point per $1, or custom rate)
        points_earned = int(amount)  # Simple: 1 point per $1
        
        return JsonResponse({
            'success': True,
            'points_earned': points_earned,
            'points_used': points_used
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in calculate_loyalty_points: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        }, status=500)


@apply_rate_limit('20/m', 'GET')
@require_http_methods(["GET"])
def create_khqr(request):
    """Create KHQR payment code"""
    try:
        # Get and validate amount
        amount_str = request.GET.get('amount', '0')
        try:
            amount_decimal = Decimal(str(amount_str))
            # Round to 2 decimal places to avoid floating-point precision issues
            amount = float(amount_decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        except (ValueError, TypeError, Exception) as e:
            return JsonResponse({
                'error': True,
                'message': 'Invalid amount format',
                'code': 'INVALID_AMOUNT'
            }, status=400)
        
        if amount <= 0:
            return JsonResponse({
                'error': True,
                'message': 'Amount must be greater than 0',
                'code': 'INVALID_AMOUNT'
            }, status=400)
        
        bakong_id = request.GET.get('bakongid', BAKONG_ID)
        merchant_name = request.GET.get('merchantname', BAKONG_MERCHANT_NAME)
        currency = request.GET.get('currency', 'USD')
        
        # Validate currency
        if currency not in ['USD', 'KHR']:
            currency = 'USD'
        
        # Bakong API minimum amount requirement (typically $0.10 for USD)
        MIN_AMOUNT_USD = 0.10
        MIN_AMOUNT_KHR = 400
        
        min_amount = MIN_AMOUNT_USD if currency == 'USD' else MIN_AMOUNT_KHR
        
        # Compare rounded amounts to avoid floating-point precision issues
        if amount < min_amount:
            return JsonResponse({
                'error': True,
                'message': f'Amount must be at least ${min_amount:.2f} USD' if currency == 'USD' else f'Amount must be at least {min_amount} KHR',
                'code': 'AMOUNT_TOO_LOW'
            }, status=400)
        
        # Call Bakong API
        url = f"{BAKONG_API_BASE}/api/khqr/create"
        params = {
            'amount': amount,
            'bakongid': bakong_id,
            'merchantname': merchant_name,
            'currency': currency
        }
        
        # Add headers to avoid 403
        headers = {
            'User-Agent': 'MADAM-DA-Ecommerce/1.0',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        # Try to parse response even if status is not 200
        try:
            data = response.json()
        except ValueError:
            data = {'error': True, 'message': response.text or f'HTTP {response.status_code}'}
        
        # Check HTTP status
        if response.status_code == 403:
            error_message = data.get('message', 'Access forbidden. Check Bakong ID and merchant name.')
            return JsonResponse({
                'error': True,
                'message': error_message,
                'code': 'FORBIDDEN',
                'details': {
                    'bakong_id': bakong_id,
                    'merchant_name': merchant_name,
                    'status_code': 403
                }
            }, status=403)
        
        elif response.status_code != 200:
            error_message = data.get('message', f'Payment gateway returned status {response.status_code}')
            return JsonResponse({
                'error': True,
                'message': error_message,
                'code': data.get('code', 'HTTP_ERROR'),
                'status_code': response.status_code
            }, status=response.status_code)
        
        # Check for errors from Bakong API
        if data.get('error'):
            error_message = data.get('message', 'Payment generation failed')
            error_code = data.get('code', 'UNKNOWN_ERROR')
            
            if 'invalid' in error_message.lower() and 'amount' in error_message.lower():
                error_message = f'Amount is invalid. The Bakong API requires a minimum payment amount (typically $0.10 USD). Your amount: ${amount:.2f}'
                error_code = 'INVALID_AMOUNT'
            
            return JsonResponse({
                'error': True,
                'message': error_message,
                'code': error_code,
                'details': {
                    'amount': amount,
                    'currency': currency
                }
            }, status=400)
        
        # Validate required fields in response
        if not data.get('qr') or not data.get('md5'):
            return JsonResponse({
                'error': True,
                'message': 'Invalid response from payment gateway: missing QR or MD5',
                'code': 'INVALID_RESPONSE'
            }, status=500)
        
        return JsonResponse(data)
        
    except requests.exceptions.Timeout:
        return JsonResponse({
            'error': True,
            'message': 'Request timeout: Payment gateway did not respond in time',
            'code': 'TIMEOUT_ERROR'
        }, status=504)
    except requests.exceptions.ConnectionError:
        return JsonResponse({
            'error': True,
            'message': 'Connection error: Could not reach payment gateway',
            'code': 'CONNECTION_ERROR'
        }, status=503)
    except Exception as e:
        logger.error(f"Error in create_khqr: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': True,
            'message': f'An error occurred: {str(e)}',
            'code': 'SERVER_ERROR'
        }, status=500)


@apply_rate_limit('30/m', 'GET')
@require_http_methods(["GET"])
def check_payment(request):
    """Check payment status"""
    try:
        md5 = request.GET.get('md5', '').strip()
        bakong_id = request.GET.get('bakongid', BAKONG_ID)
        
        # Validate MD5
        if not md5:
            return JsonResponse({
                'error': True,
                'message': 'MD5 hash is required',
                'code': 'MISSING_MD5'
            }, status=400)
        
        if len(md5) != 32:
            return JsonResponse({
                'error': True,
                'message': 'Invalid MD5 hash format (must be 32 characters)',
                'code': 'INVALID_MD5'
            }, status=400)
        
        # Call Bakong API
        url = f"{BAKONG_API_BASE}/api/khqr/check"
        params = {
            'md5': md5,
            'bakongid': bakong_id
        }
        
        # Add headers to avoid 403
        headers = {
            'User-Agent': 'MADAM-DA-Ecommerce/1.0',
            'Accept': 'application/json',
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        # Try to parse response even if status is not 200
        try:
            data = response.json()
        except ValueError:
            data = {'error': True, 'message': response.text or f'HTTP {response.status_code}'}
        
        # Check HTTP status
        if response.status_code == 403:
            return JsonResponse({
                'error': True,
                'message': 'Access forbidden. Check Bakong ID.',
                'code': 'FORBIDDEN',
                'status_code': 403
            }, status=403)
        
        elif response.status_code != 200:
            error_message = data.get('message', f'Payment gateway returned status {response.status_code}')
            return JsonResponse({
                'error': True,
                'message': error_message,
                'code': data.get('code', 'HTTP_ERROR'),
                'status_code': response.status_code
            }, status=response.status_code)
        
        # Check for errors from Bakong API
        if data.get('error'):
            error_message = data.get('message', 'Payment check failed')
            error_code = data.get('code', 'UNKNOWN_ERROR')
            
            # Handle MD5_NOT_FOUND as a normal case (payment not yet made)
            if error_code == 'MD5_NOT_FOUND':
                return JsonResponse({
                    'error': False,
                    'responseCode': -1,
                    'message': 'Payment not found or not yet completed'
                })
            
            return JsonResponse({
                'error': True,
                'message': error_message,
                'code': error_code
            }, status=400)
        
        return JsonResponse(data)
        
    except requests.exceptions.Timeout:
        return JsonResponse({
            'error': True,
            'message': 'Request timeout: Payment gateway did not respond in time',
            'code': 'TIMEOUT_ERROR'
        }, status=504)
    except requests.exceptions.ConnectionError:
        return JsonResponse({
            'error': True,
            'message': 'Connection error: Could not reach payment gateway',
            'code': 'CONNECTION_ERROR'
        }, status=503)
    except Exception as e:
        logger.error(f"Error in check_payment: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': True,
            'message': f'An error occurred: {str(e)}',
            'code': 'SERVER_ERROR'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_order_on_payment(request):
    """Create order when payment is confirmed - called from frontend"""
    try:
        data = json.loads(request.body)
        
        # Get order data
        name = escape(data.get('name', '').strip())
        phone = escape(data.get('phone', '').strip())
        address = escape(data.get('address', '').strip())
        province = escape(data.get('province', '').strip())
        payment_method = data.get('payment_method', 'KHQR')
        total = Decimal(str(data.get('total', 0)))
        subtotal = Decimal(str(data.get('subtotal', 0)))
        discount_amount = Decimal(str(data.get('discount', 0)))
        items = data.get('items', [])
        
        # Validate required fields
        if not all([name, phone, address, province]):
            return JsonResponse({
                'error': True,
                'message': 'Missing required fields'
            }, status=400)
        
        if not items:
            return JsonResponse({
                'error': True,
                'message': 'No items in order'
            }, status=400)
        
        # Get or create customer
        customer, _ = Customer.objects.get_or_create(
            phone=phone,
            defaults={'name': name, 'address': address, 'province': province}
        )
        
        # Determine order status based on payment method
        if payment_method == 'Cash on Delivery':
            order_status = 'pending'
        else:
            order_status = 'confirmed'
        
        # Create order WITHOUT order_number - let the model's save() method generate it sequentially
        order = Order(
            customer=customer,
            customer_name=name,
            customer_phone=phone,
            customer_address=address,
            customer_province=province,
            subtotal=subtotal,
            shipping_fee=Decimal('0.00'),
            discount_amount=discount_amount,
            total=total,
            payment_method=payment_method,
            status=order_status,
            customer_received=False,  # Explicitly set to False for new orders
            payment_received=False  # Explicitly set to False for new orders
        )
        # Save to trigger order_number generation (sequential)
        order.save()
        
        # Send WebSocket message for new order
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            if channel_layer:
                # Get order items
                items_data = []
                for item_data in items:
                    product_name = item_data.get('name', 'Unknown Product')
                    quantity = item_data.get('qty', 1)
                    price = Decimal(str(item_data.get('price', 0)))
                    subtotal = price * quantity
                    
                    items_data.append({
                        'product_name': product_name,
                        'quantity': quantity,
                        'price': str(price),
                        'subtotal': str(subtotal)
                    })
                
                order_data = {
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'status': order.status,
                    'status_display': order.get_status_display(),
                    'customer_name': order.customer_name,
                    'customer_phone': order.customer_phone,
                    'customer_address': order.customer_address,
                    'customer_province': order.customer_province,
                    'total_amount': str(order.total),
                    'payment_method': order.payment_method,
                    'created_at': order.created_at.isoformat(),
                    'items': items_data
                }
                
                async_to_sync(channel_layer.group_send)(
                    'orders_updates',
                    {
                        'type': 'new_order',
                        'order': order_data
                    }
                )
        except Exception as e:
            logger.error(f"Error sending WebSocket message for new order: {str(e)}", exc_info=True)
        
        # Check if order is suspicious
        order.check_suspicious()
        order.save()
        
        # Create order items
        for item in items:
            product_id = item.get('id')
            product_name = item.get('name', 'Unknown Product')
            product_price = Decimal(str(item.get('price', 0)))
            quantity = int(item.get('qty', 1))
            
            product = None
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    pass
            
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product_name,
                product_price=product_price,
                quantity=quantity,
                subtotal=product_price * quantity
            )
        
        # Send WebSocket message for new order
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            
            channel_layer = get_channel_layer()
            if channel_layer:
                # Get order items
                items_data = []
                for item in items:
                    product_name = item.get('name', 'Unknown Product')
                    quantity = int(item.get('qty', 1))
                    price = Decimal(str(item.get('price', 0)))
                    subtotal = price * quantity
                    
                    items_data.append({
                        'product_name': product_name,
                        'quantity': quantity,
                        'price': str(price),
                        'subtotal': str(subtotal)
                    })
                
                order.refresh_from_db()
                order_data = {
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'status': order.status,
                    'status_display': order.get_status_display(),
                    'customer_name': order.customer_name,
                    'customer_phone': order.customer_phone,
                    'customer_address': order.customer_address,
                    'customer_province': order.customer_province,
                    'total_amount': str(order.total),
                    'payment_method': order.payment_method,
                    'created_at': order.created_at.isoformat(),
                    'items': items_data
                }
                
                async_to_sync(channel_layer.group_send)(
                    'orders_updates',
                    {
                        'type': 'new_order',
                        'order': order_data
                    }
                )
        except Exception as e:
            logger.error(f"Error sending WebSocket message for new order: {str(e)}", exc_info=True)
        
        # Send Telegram notification immediately when payment is confirmed
        order.refresh_from_db()
        try:
            logger.info(f"Payment confirmed - Order created: {order.order_number}, sending Telegram notification...")
            send_telegram_notification(order)
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'message': 'Order created successfully'
        })
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON data received for order creation.")
        return JsonResponse({
            'error': True,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error creating order on payment: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': True,
            'message': f'An error occurred: {str(e)}'
        }, status=500)


# ========== COD (Cash on Delivery) Automation Views ==========

@csrf_exempt
@require_http_methods(["GET", "POST"])
def cod_confirmation_view(request, order_number=None):
    """Mobile-friendly page for delivery drivers to confirm COD payment"""
    if request.method == 'GET':
        # Check for auto-confirm parameter (from QR scan)
        auto_confirm = request.GET.get('auto_confirm', '').lower() == 'true'
        
        # Show confirmation form
        order = None
        if order_number:
            try:
                order = Order.objects.get(order_number=order_number, payment_method='Cash on Delivery')
                
                # Auto-confirm if requested and order is not already paid
                if auto_confirm and not order.payment_received:
                    # Auto-confirm payment via API
                    from django.http import JsonResponse
                    try:
                        # Use the same logic as cod_confirm_api
                        order.payment_received = True
                        order.payment_received_at = timezone.now()
                        order.payment_received_by = 'QR Scanner'
                        
                        # Also mark customer as received
                        if not order.customer_received:
                            order.customer_received = True
                            order.customer_received_at = timezone.now()
                            order.customer_received_by = 'QR Scanner'
                        
                        order.status = 'confirmed'
                        order.save()
                        
                        # Send WebSocket message
                        try:
                            from channels.layers import get_channel_layer
                            from asgiref.sync import async_to_sync
                            
                            channel_layer = get_channel_layer()
                            if channel_layer:
                                items = order.items.all()
                                items_data = [{
                                    'product_name': item.product_name,
                                    'quantity': item.quantity,
                                    'price': str(item.product_price),
                                    'subtotal': str(item.subtotal)
                                } for item in items]
                                
                                order_data = {
                                    'order_id': order.id,
                                    'order_number': order.order_number,
                                    'status': order.status,
                                    'status_display': order.get_status_display(),
                                    'customer_name': order.customer_name,
                                    'customer_phone': order.customer_phone,
                                    'customer_address': order.customer_address,
                                    'customer_province': order.customer_province,
                                    'total_amount': str(order.total),
                                    'payment_method': order.payment_method,
                                    'created_at': order.created_at.isoformat(),
                                    'items': items_data,
                                    'payment_received': order.payment_received,
                                    'payment_received_at': order.payment_received_at.isoformat() if order.payment_received_at else None,
                                    'customer_received': order.customer_received,
                                    'customer_received_at': order.customer_received_at.isoformat() if order.customer_received_at else None,
                                }
                                
                                async_to_sync(channel_layer.group_send)(
                                    'orders_updates',
                                    {
                                        'type': 'payment_confirmed',
                                        'order': order_data
                                    }
                                )
                        except Exception:
                            pass
                        
                        # Refresh order from database
                        order.refresh_from_db()
                    except Exception as e:
                        # If auto-confirm fails, just show the form
                        import logging
                        logger = logging.getLogger(__name__)
                        logger.error(f'Error auto-confirming payment: {e}')
            except Order.DoesNotExist:
                pass
        
        auto_confirmed = False
        if order and order.payment_received:
            # Check if payment was just confirmed (within last 5 seconds) or if auto_confirm param is present
            if auto_confirm or (order.payment_received_at and (timezone.now() - order.payment_received_at).total_seconds() < 5):
                auto_confirmed = True
        
        return render(request, 'app/cod_confirmation.html', {
            'order': order,
            'order_number': order_number or '',
            'auto_confirmed': auto_confirmed
        })
    
    elif request.method == 'POST':
        # Handle payment confirmation
        order_num = request.POST.get('order_number', '').strip().upper()
        driver_name = request.POST.get('driver_name', '').strip()
        notes = request.POST.get('notes', '').strip()
        
        if not order_num:
            return JsonResponse({'success': False, 'message': 'Order number is required'}, status=400)
        
        try:
            order = Order.objects.get(order_number=order_num, payment_method='Cash on Delivery')
            
            if order.payment_received:
                return JsonResponse({
                    'success': False, 
                    'message': f'Order {order_num} is already marked as paid'
                }, status=400)
            
            # Confirm payment
            order.payment_received = True
            order.payment_received_at = timezone.now()
            order.payment_received_by = driver_name or 'Driver'
            if notes:
                order.cod_delivery_notes = notes
            
            # NOTE: Do NOT automatically mark customer as received when payment is confirmed
            # Payment and delivery/receipt are separate events. A customer can pay but not have received the order yet.
            # Customer received status should only be set when the order status changes to "delivered" or explicitly marked.
            
            order.status = 'confirmed'
            order.save()
            
            # Send WebSocket message for payment confirmation
            try:
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                
                channel_layer = get_channel_layer()
                if channel_layer:
                    # Get order items for the message
                    items = order.items.all()
                    items_data = [{
                        'product_name': item.product_name,
                        'quantity': item.quantity,
                        'price': str(item.product_price),
                        'subtotal': str(item.subtotal)
                    } for item in items]
                    
                    order_data = {
                        'order_id': order.id,
                        'order_number': order.order_number,
                        'status': order.status,
                        'status_display': order.get_status_display(),
                        'customer_name': order.customer_name,
                        'customer_phone': order.customer_phone,
                        'total_amount': str(order.total),
                        'payment_method': order.payment_method,
                        'created_at': order.created_at.isoformat(),
                        'items': items_data,
                        'payment_received': order.payment_received,
                        'payment_received_at': order.payment_received_at.isoformat() if order.payment_received_at else None,
                        'customer_received': order.customer_received,
                        'customer_received_at': order.customer_received_at.isoformat() if order.customer_received_at else None,
                    }
                    
                    async_to_sync(channel_layer.group_send)(
                        'orders_updates',
                        {
                            'type': 'payment_confirmed',
                            'order': order_data
                        }
                    )
            except Exception as e:
                # WebSocket failure shouldn't break payment confirmation
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error sending WebSocket message: {e}')
            
            # Send Telegram notification
            try:
                send_telegram_notification(order)
            except:
                pass
            
            return JsonResponse({
                'success': True,
                'message': f'Payment confirmed for order {order_num}',
                'order': {
                    'number': order.order_number,
                    'total': str(order.total),
                    'customer': order.customer_name
                }
            })
            
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': f'Order {order_num} not found or not a COD order'
            }, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def cod_confirm_api(request):
    """API endpoint for COD payment confirmation (for mobile apps)"""
    try:
        data = json.loads(request.body)
        order_number = data.get('order_number', '').strip().upper()
        driver_name = data.get('driver_name', '').strip()
        notes = data.get('notes', '').strip()
        
        if not order_number:
            return JsonResponse({
                'success': False,
                'message': 'Order number is required'
            }, status=400)
        
        try:
            order = Order.objects.get(order_number=order_number, payment_method='Cash on Delivery')
            
            if order.payment_received:
                return JsonResponse({
                    'success': False,
                    'message': 'Order already marked as paid'
                }, status=400)
            
            # Confirm payment
            order.payment_received = True
            order.payment_received_at = timezone.now()
            order.payment_received_by = driver_name or 'API'
            if notes:
                order.cod_delivery_notes = notes
            
            # NOTE: Do NOT automatically mark customer as received when payment is confirmed
            # Payment and delivery/receipt are separate events. A customer can pay but not have received the order yet.
            # Customer received status should only be set when the order status changes to "delivered" or explicitly marked.
            
            order.status = 'confirmed'
            order.save()
            
            # Send WebSocket message for payment confirmation
            try:
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                
                channel_layer = get_channel_layer()
                if channel_layer:
                    # Get order items for the message
                    items = order.items.all()
                    items_data = [{
                        'product_name': item.product_name,
                        'quantity': item.quantity,
                        'price': str(item.product_price),
                        'subtotal': str(item.subtotal)
                    } for item in items]
                    
                    order_data = {
                        'order_id': order.id,
                        'order_number': order.order_number,
                        'status': order.status,
                        'status_display': order.get_status_display(),
                        'customer_name': order.customer_name,
                        'customer_phone': order.customer_phone,
                        'customer_address': order.customer_address,
                        'customer_province': order.customer_province,
                        'total_amount': str(order.total),
                        'payment_method': order.payment_method,
                        'created_at': order.created_at.isoformat(),
                        'items': items_data,
                        'payment_received': order.payment_received,
                        'payment_received_at': order.payment_received_at.isoformat() if order.payment_received_at else None,
                        'customer_received': order.customer_received,
                        'customer_received_at': order.customer_received_at.isoformat() if order.customer_received_at else None,
                    }
                    
                    async_to_sync(channel_layer.group_send)(
                        'orders_updates',
                        {
                            'type': 'payment_confirmed',
                            'order': order_data
                        }
                    )
            except Exception as e:
                # WebSocket failure shouldn't break payment confirmation
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error sending WebSocket message: {e}')
            
            return JsonResponse({
                'success': True,
                'message': 'Payment confirmed',
                'order_number': order.order_number,
                'total': str(order.total)
            })
            
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Order not found'
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)


@require_http_methods(["GET"])
def cod_qr_view(request, order_number):
    """Generate QR code for COD order confirmation"""
    try:
        order = Order.objects.get(order_number=order_number, payment_method='Cash on Delivery')
        
        # Generate QR code data (URL to confirmation page)
        qr_data = f"{request.scheme}://{request.get_host()}/cod/confirm/{order_number}/"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
        
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


@require_http_methods(["GET"])
def cod_print_view(request, order_number):
    """Printable page with QR code for COD order"""
    try:
        order = Order.objects.get(order_number=order_number, payment_method='Cash on Delivery')
        
        # Generate QR code URL
        qr_url = f"{request.scheme}://{request.get_host()}/cod/qr/{order_number}/"
        confirm_url = f"{request.scheme}://{request.get_host()}/cod/confirm/{order_number}/"
        
        context = {
            'order': order,
            'qr_url': qr_url,
            'confirm_url': confirm_url,
        }
        return render(request, 'app/cod_print.html', context)
        
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)


# ========== ORDER TRACKING FOR CUSTOMERS ==========

@require_http_methods(["GET"])
def track_order_view(request):
    """Page for customers to track their order"""
    order_number = request.GET.get('order', '')
    phone = request.GET.get('phone', '')
    
    context = {
        'order_number': order_number,
        'phone': phone,
    }
    return render(request, 'app/track_order.html', context)


@csrf_exempt
@require_http_methods(["GET"])
@apply_rate_limit('60/m', 'GET')
def customer_lookup(request):
    """API endpoint to lookup customer by phone number for auto-fill"""
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
        
        # Try to find customer by phone (exact match or normalized)
        try:
            # First try exact match
            customer = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            # Try normalized phone
            try:
                customer = Customer.objects.filter(phone__icontains=normalized_phone).first()
            except:
                customer = None
        
        # If still not found, try to find from recent orders
        if not customer:
            try:
                # Get the most recent order with this phone number
                order = Order.objects.filter(
                    customer_phone__icontains=normalized_phone
                ).order_by('-created_at').first()
                
                if order:
                    # Return customer data from order
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
            # Customer not found - return success: false but don't error
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


@csrf_exempt
@require_http_methods(["POST"])
def track_order_api(request):
    """API endpoint for customers to track their order by order number and phone"""
    try:
        data = json.loads(request.body)
        order_number = data.get('order_number', '').strip().upper()
        phone = data.get('phone', '').strip()
        
        if not order_number or not phone:
            return JsonResponse({
                'success': False,
                'message': 'Order number and phone number are required'
            }, status=400)
        
        # Normalize phone number (remove spaces, dashes, etc.)
        normalized_phone = ''.join(filter(str.isdigit, phone))
        
        try:
            order = Order.objects.get(order_number=order_number)
            
            # Verify phone number matches
            order_phone_normalized = ''.join(filter(str.isdigit, order.customer_phone))
            
            if normalized_phone != order_phone_normalized:
                return JsonResponse({
                    'success': False,
                    'message': 'Phone number does not match this order'
                }, status=403)
            
            # Get order items
            items = OrderItem.objects.filter(order=order).select_related('product')
            items_data = [{
                'product_name': item.product.name if item.product else item.product_name,
                'quantity': item.quantity,
                'price': str(item.product_price),
                'subtotal': str(item.subtotal)
            } for item in items]
            
            # Return order details
            return JsonResponse({
                'success': True,
                'order': {
                    'order_number': order.order_number,
                    'customer_name': order.customer_name,
                    'customer_phone': order.customer_phone,
                    'customer_address': order.customer_address or '',
                    'customer_province': order.customer_province or '',
                    'status': order.status,
                    'status_display': order.get_status_display(),
                    'payment_method': order.payment_method,
                    'payment_received': order.payment_received,
                    'payment_received_at': order.payment_received_at.isoformat() if order.payment_received_at else None,
                    'customer_received': order.customer_received,
                    'customer_received_at': order.customer_received_at.isoformat() if order.customer_received_at else None,
                    'subtotal': str(order.subtotal),
                    'shipping_fee': str(order.shipping_fee),
                    'discount_amount': str(order.discount_amount),
                    'total': str(order.total),
                    'created_at': order.created_at.isoformat(),
                    'updated_at': order.updated_at.isoformat(),
                    'items': items_data
                }
            })
            
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Order not found'
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Error in track_order_api: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while tracking your order'
        }, status=500)
