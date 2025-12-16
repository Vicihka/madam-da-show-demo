"""
Custom exceptions for the MADAM DA E-Commerce application
"""


class PaymentError(Exception):
    """Base class for payment-related errors"""
    pass


class PaymentTimeoutError(PaymentError):
    """Payment request timed out"""
    pass


class PaymentDeclinedError(PaymentError):
    """Payment was declined"""
    pass


class PaymentConnectionError(PaymentError):
    """Cannot connect to payment service"""
    pass


class InsufficientStockError(Exception):
    """Product stock is insufficient"""
    pass


class InvalidPromoCodeError(Exception):
    """Promo code is invalid"""
    pass


class OrderCreationError(Exception):
    """Order creation failed"""
    pass


class StockValidationError(Exception):
    """Stock validation failed"""
    pass


class InvalidPromoCodeError(Exception):
    """Promo code is invalid"""
    pass
