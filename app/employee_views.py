"""
Employee Dashboard Views
Simple interface for employees to manage orders and print QR codes
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q, Prefetch
from django.core.exceptions import ValidationError
from .models import Order, OrderItem
import json
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def employee_dashboard(request):
    """Main employee dashboard - shows orders that need action"""
    
    # Maximum orders to load per status (prevents memory issues with 1000+ orders)
    MAX_ORDERS_PER_STATUS = 100
    
    # Get orders that need preparation (confirmed or pending)
    # Exclude orders that are already received by customer
    # Optimized with select_related and prefetch_related for better performance
    # LIMITED to prevent loading too many orders at once
    orders_to_prepare = Order.objects.filter(
        status__in=['pending', 'confirmed']
    ).exclude(status='cancelled').exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product'))
    ).order_by('-created_at')[:MAX_ORDERS_PER_STATUS]
    
    # Get orders being prepared
    # Exclude orders that are already received by customer
    orders_preparing = Order.objects.filter(
        status='preparing'
    ).exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related(
        Prefetch('items', queryset=OrderItem.objects.select_related('product'))
    ).order_by('-created_at')[:MAX_ORDERS_PER_STATUS]
    
    # Get orders ready for delivery
    # Exclude orders that are already received by customer
    orders_ready = Order.objects.filter(
        status='ready_for_delivery'
    ).exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related('items').order_by('-created_at')[:MAX_ORDERS_PER_STATUS]
    
    # Get orders out for delivery
    # Exclude orders that are already received by customer
    orders_out = Order.objects.filter(
        status='out_for_delivery'
    ).exclude(customer_received=True).select_related(
        'customer', 'promo_code'
    ).prefetch_related('items').order_by('-created_at')[:MAX_ORDERS_PER_STATUS]
    
    # Get delivered orders (show ALL delivered orders from last 7 days, not just today)
    # This ensures delivered orders persist even after page refresh
    from datetime import timedelta
    seven_days_ago = timezone.now() - timedelta(days=7)
    orders_delivered_today = Order.objects.filter(
        status='delivered',
        updated_at__gte=seven_days_ago  # Show orders delivered in last 7 days
    ).select_related(
        'customer', 'promo_code'
    ).prefetch_related('items').order_by('-updated_at')[:50]  # Order by updated_at (when delivered)
    
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


@require_http_methods(["GET"])
def employee_order_detail(request, order_number):
    """View order details for employee"""
    order = get_object_or_404(Order, order_number=order_number)
    items = OrderItem.objects.filter(order=order)
    
    # Check if COD and needs QR code
    needs_qr = (
        order.payment_method == 'Cash on Delivery' and 
        not order.payment_received and
        order.status in ['preparing', 'ready_for_delivery', 'out_for_delivery']
    )
    
    context = {
        'order': order,
        'items': items,
        'needs_qr': needs_qr,
    }
    
    return render(request, 'app/employee_order_detail.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def employee_update_status(request, order_number):
    """API endpoint for employees to update order status"""
    try:
        data = json.loads(request.body)
        new_status = data.get('status', '').strip()
        
        if new_status not in ['preparing', 'ready_for_delivery', 'out_for_delivery', 'delivered']:
            return JsonResponse({
                'success': False,
                'message': 'Invalid status'
            }, status=400)
        
        order = get_object_or_404(Order, order_number=order_number)
        old_status = order.status
        
        # Validate status transition
        try:
            order.validate_status_transition(new_status)
        except ValidationError as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
        
        order.status = new_status
        
        # When order is marked as 'delivered', automatically set customer_received=True
        # This makes sense because "delivered" means the customer received the order
        if new_status == 'delivered' and not order.customer_received:
            order.customer_received = True
            order.customer_received_at = timezone.now()
            order.customer_received_by = 'Employee Dashboard (Auto)'
        
        try:
            order.save()
        except Exception as e:
            logger.error(f"Error saving order {order_number}: {str(e)}", exc_info=True)
            return JsonResponse({
                'success': False,
                'message': f'Error updating order: {str(e)}'
            }, status=500)
        
        # Send WebSocket message to all connected dashboards
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        if channel_layer:
            # Get order items for the message
            items = OrderItem.objects.filter(order=order)
            items_data = [{
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': str(item.product_price),
                'subtotal': str(item.subtotal)
            } for item in items]
            
            # Refresh order from database to get updated customer_received status
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
                'items': items_data,
                'customer_received': order.customer_received,
                'customer_received_at': order.customer_received_at.isoformat() if order.customer_received_at else None,
                'customer_received_by': order.customer_received_by,
                'payment_received': order.payment_received,
                'payment_received_at': order.payment_received_at.isoformat() if order.payment_received_at else None,
            }
            
            async_to_sync(channel_layer.group_send)(
                'orders_updates',
                {
                    'type': 'status_changed',
                    'order': order_data,
                    'old_status': old_status,
                    'new_status': new_status
                }
            )
        
        return JsonResponse({
            'success': True,
            'message': f'Order status updated from {old_status} to {new_status}',
            'order_number': order.order_number,
            'status': order.status
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@require_http_methods(["GET"])
def employee_print_qr(request, order_number):
    """Print QR code page for employee"""
    order = get_object_or_404(Order, order_number=order_number)
    
    if order.payment_method != 'Cash on Delivery':
        return JsonResponse({
            'error': 'This order is not Cash on Delivery'
        }, status=400)
    
    # Generate QR code URL
    qr_url = f"{request.scheme}://{request.get_host()}/cod/qr/{order_number}/"
    confirm_url = f"{request.scheme}://{request.get_host()}/cod/confirm/{order_number}/"
    
    context = {
        'order': order,
        'qr_url': qr_url,
        'confirm_url': confirm_url,
        'employee_view': True,
    }
    
    return render(request, 'app/cod_print.html', context)


def serialize_order(order):
    """Helper function to serialize order data for API responses"""
    items = [{
        'product_name': item.product_name,
        'quantity': item.quantity,
        'price': str(item.product_price),
        'subtotal': str(item.subtotal)
    } for item in order.items.all()]
    
    return {
        'order_number': order.order_number,
        'customer_name': order.customer_name,
        'customer_phone': order.customer_phone,
        'customer_address': order.customer_address,
        'customer_province': order.customer_province,
        'total': str(order.total),
        'total_amount': str(order.total),  # For compatibility
        'payment_method': order.payment_method,
        'status': order.status,
        'status_display': order.get_status_display(),
        'created_at': order.created_at.isoformat(),
        'items': items,
        'customer_received': order.customer_received,
        'customer_received_at': order.customer_received_at.isoformat() if order.customer_received_at else None,
        'customer_received_by': order.customer_received_by,
        'payment_received': order.payment_received,
        'payment_received_at': order.payment_received_at.isoformat() if order.payment_received_at else None,
    }


@require_http_methods(["GET"])
def employee_dashboard_api(request):
    """API endpoint for real-time order updates"""
    try:
        # Get orders that need preparation
        # Exclude orders that are already received by customer
        # Optimized with select_related and prefetch_related for better performance
        orders_to_prepare = Order.objects.filter(
            status__in=['pending', 'confirmed']
        ).exclude(status='cancelled').exclude(customer_received=True).select_related(
            'customer', 'promo_code'
        ).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product'))
        ).order_by('-created_at')
        
        # Get orders being prepared
        # Exclude orders that are already received by customer
        orders_preparing = Order.objects.filter(
            status='preparing'
        ).exclude(customer_received=True).select_related(
            'customer', 'promo_code'
        ).prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product'))
        ).order_by('-created_at')
        
        # Get orders ready for delivery
        # Exclude orders that are already received by customer
        orders_ready = Order.objects.filter(
            status='ready_for_delivery'
        ).exclude(customer_received=True).select_related(
            'customer', 'promo_code'
        ).prefetch_related('items').order_by('-created_at')
        
        # Get orders out for delivery
        # Exclude orders that are already received by customer
        orders_out = Order.objects.filter(
            status='out_for_delivery'
        ).exclude(customer_received=True).select_related(
            'customer', 'promo_code'
        ).prefetch_related('items').order_by('-created_at')
        
        # Get delivered orders (show ALL delivered orders from last 7 days)
        # This ensures delivered orders persist even after page refresh
        from datetime import timedelta
        seven_days_ago = timezone.now() - timedelta(days=7)
        orders_delivered = Order.objects.filter(
            status='delivered',
            updated_at__gte=seven_days_ago  # Show orders delivered in last 7 days
        ).select_related(
            'customer', 'promo_code'
        ).prefetch_related('items').order_by('-updated_at')[:50]  # Order by updated_at (when delivered)
        
        return JsonResponse({
            'success': True,
            'stats': {
                'total_to_prepare': orders_to_prepare.count(),
                'total_preparing': orders_preparing.count(),
                'total_ready': orders_ready.count(),
                'total_out': orders_out.count(),
            },
            'orders_to_prepare': [serialize_order(o) for o in orders_to_prepare],
            'orders_preparing': [serialize_order(o) for o in orders_preparing],
            'orders_ready': [serialize_order(o) for o in orders_ready],
            'orders_out': [serialize_order(o) for o in orders_out],
            'orders_delivered': [serialize_order(o) for o in orders_delivered],
        })
    except Exception as e:
        logger.error(f"Error in employee_dashboard_api: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'message': 'Error fetching orders. Please try again.',
            'error': str(e) if settings.DEBUG else None
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def employee_confirm_payment(request, order_number):
    """API endpoint for employees to confirm COD payment"""
    try:
        data = json.loads(request.body)
        notes = data.get('notes', '').strip()
        
        order = get_object_or_404(Order, order_number=order_number)
        
        # Check if it's a COD order
        if order.payment_method != 'Cash on Delivery':
            return JsonResponse({
                'success': False,
                'message': 'This order is not Cash on Delivery'
            }, status=400)
        
        # Check if already paid - return success if already confirmed (idempotent)
        if order.payment_received:
            return JsonResponse({
                'success': True,
                'message': 'Payment was already confirmed for this order',
                'order_number': order.order_number,
                'total': str(order.total),
                'already_confirmed': True
            })
        
        # Confirm payment
        order.payment_received = True
        order.payment_received_at = timezone.now()
        order.payment_received_by = 'Employee Dashboard'
        if notes:
            order.cod_delivery_notes = notes
        
        # NOTE: Do NOT automatically mark customer as received when payment is confirmed
        # Payment and delivery/receipt are separate events. A customer can pay but not have received the order yet.
        # Customer received status should only be set when the order status changes to "delivered" or explicitly marked.
        
        order.save()
        
        # Send WebSocket message for payment confirmation
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        if channel_layer:
            # Get order items for the message
            items = OrderItem.objects.filter(order=order)
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
        
        return JsonResponse({
            'success': True,
            'message': 'Payment confirmed successfully',
            'order_number': order.order_number,
            'total': str(order.total)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

