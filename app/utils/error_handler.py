"""
Centralized error handling utilities for MADAM DA E-Commerce
"""
import logging
from django.http import JsonResponse
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import DatabaseError, IntegrityError
from requests.exceptions import Timeout, ConnectionError as RequestsConnectionError
import uuid

from ..exceptions import (
    PaymentError, PaymentTimeoutError, PaymentDeclinedError, PaymentConnectionError,
    InsufficientStockError, InvalidPromoCodeError, OrderCreationError, StockValidationError
)

logger = logging.getLogger(__name__)


def handle_api_error(error, context=None, request_id=None):
    """
    Handle API errors consistently
    
    Args:
        error: Exception object
        context: Additional context dict (for logging)
        request_id: Optional request ID for tracking
    
    Returns:
        JsonResponse with error details
    """
    if request_id is None:
        request_id = str(uuid.uuid4())[:8]
    
    error_type = type(error).__name__
    
    # Prepare context for logging
    log_context = {
        'request_id': request_id,
        'error_type': error_type,
    }
    if context:
        log_context.update(context)
    
    # Log error with full details
    logger.error(
        f"API Error [{request_id}]: {error_type} - {str(error)}",
        exc_info=True,
        extra=log_context
    )
    
    # Map exceptions to HTTP status codes and user-friendly messages
    error_map = {
        # Django exceptions
        'ValidationError': (400, 'Validation failed. Please check your input.'),
        'DoesNotExist': (404, 'Resource not found.'),
        'PermissionDenied': (403, 'Permission denied.'),
        'IntegrityError': (400, 'Database integrity error. Please try again.'),
        'DatabaseError': (500, 'Database error. Please try again later.'),
        
        # Custom exceptions
        'InsufficientStockError': (400, str(error) or 'Product is out of stock.'),
        'InvalidPromoCodeError': (400, str(error) or 'Invalid promo code.'),
        'OrderCreationError': (500, 'Order creation failed. Please try again.'),
        'StockValidationError': (400, str(error) or 'Stock validation failed.'),
        
        # Payment exceptions
        'PaymentTimeoutError': (504, 'Payment processing timed out. Please try again.'),
        'PaymentDeclinedError': (402, 'Payment was declined. Please check your payment method.'),
        'PaymentConnectionError': (503, 'Payment service is temporarily unavailable. Please try again later.'),
        'PaymentError': (500, 'Payment processing error. Please try again.'),
        
        # Requests exceptions
        'Timeout': (504, 'Request timeout. Please try again.'),
        'ConnectionError': (503, 'Service unavailable. Please try again later.'),
        'RequestsConnectionError': (503, 'Cannot connect to service. Please try again later.'),
    }
    
    status_code, default_message = error_map.get(error_type, (500, 'An error occurred. Please try again.'))
    
    # Use error message if available, otherwise use default
    message = str(error) if str(error) else default_message
    
    # Don't expose technical details in production
    from django.conf import settings
    if settings.DEBUG:
        # In debug mode, include more details
        error_response = {
            'success': False,
            'error': {
                'type': error_type,
                'message': message,
                'request_id': request_id,
            },
            'debug_info': {
                'exception': str(error),
                'context': context
            } if context else None
        }
    else:
        # In production, only show user-friendly message
        error_response = {
            'success': False,
            'error': {
                'type': error_type,
                'message': message,
                'request_id': request_id,
            }
        }
    
    return JsonResponse(error_response, status=status_code)


def safe_api_call(func):
    """
    Decorator to safely handle API calls with consistent error handling
    
    Usage:
        @safe_api_call
        def my_api_view(request):
            # Your code here
            return JsonResponse({'success': True})
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Extract request from args if available
            context = {}
            if args and hasattr(args[0], 'META'):
                request = args[0]
                context = {
                    'path': request.path,
                    'method': request.method,
                    'user': str(request.user) if hasattr(request, 'user') else 'anonymous',
                }
            return handle_api_error(e, context=context)
    return wrapper
