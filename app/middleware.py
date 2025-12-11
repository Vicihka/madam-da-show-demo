"""
Performance and Security Middleware for MADAM DA
Adds compression, caching headers, and security features.
"""

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import logging
import gzip
import os

logger = logging.getLogger(__name__)


class CompressionMiddleware(MiddlewareMixin):
    """
    Gzip compression middleware for text-based responses.
    Reduces response size by 60-80% for better performance.
    """
    
    def process_response(self, request, response):
        # Ensure UTF-8 charset is set for text responses
        content_type = response.get('Content-Type', '')
        if content_type:
            # Check if charset is missing
            if 'charset' not in content_type.lower():
                # Add charset=utf-8 to text-based content types
                if any(ct in content_type for ct in ['text/html', 'text/css', 'application/javascript', 'application/json', 'text/javascript', 'text/plain']):
                    response['Content-Type'] = f"{content_type}; charset=utf-8"
                    content_type = response.get('Content-Type', '')
        
        # Only compress text-based content
        if not any(ct in content_type for ct in ['text/html', 'text/css', 'application/javascript', 'application/json', 'text/javascript']):
            return response
        
        # Check if client accepts gzip
        accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
        if 'gzip' not in accept_encoding:
            return response
        
        # Don't compress if already compressed
        if response.get('Content-Encoding'):
            return response
        
        # Compress response
        response.content = gzip.compress(response.content)
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = str(len(response.content))
        
        return response


class CacheControlMiddleware(MiddlewareMixin):
    """
    Adds cache control headers for static assets.
    """
    
    def process_response(self, request, response):
        # Cache static files for 1 year
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
        # Cache media files for 1 month
        elif request.path.startswith('/media/'):
            response['Cache-Control'] = 'public, max-age=2592000'
        # Don't cache HTML pages
        elif response.get('Content-Type', '').startswith('text/html'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Add comprehensive security headers to all responses"""
    
    def process_response(self, request, response):
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://fonts.googleapis.com https://html2canvas.hertzen.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https: blob:; "
            "connect-src 'self' https://bakongapi.com https://bakong-khqr.web.app; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response['Content-Security-Policy'] = csp
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        # X-Frame-Options is redundant when CSP frame-ancestors is set, but kept for older browsers
        # X-XSS-Protection is deprecated and not needed with CSP
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(self)'
        
        # Remove security headers from media files (not needed and causes warnings)
        if request.path.startswith('/media/'):
            response.pop('Content-Security-Policy', None)
            response.pop('X-XSS-Protection', None)
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
        
        return response


class RequestSizeLimitMiddleware(MiddlewareMixin):
    """Limit request body size to prevent DoS attacks"""
    MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB
    
    def process_request(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_length = request.META.get('CONTENT_LENGTH', 0)
            try:
                content_length = int(content_length)
                if content_length > self.MAX_REQUEST_SIZE:
                    logger.warning(f'Request too large: {content_length} bytes from {request.META.get("REMOTE_ADDR")}')
                    return HttpResponse('Request too large', status=413)
            except (ValueError, TypeError):
                pass
        return None


class IPWhitelistMiddleware(MiddlewareMixin):
    """Restrict admin access to whitelisted IPs (optional, for extra security)"""
    
    def process_request(self, request):
        # Only apply to admin URLs
        if request.path.startswith('/admin/') or '/admin/' in request.path:
            # Get whitelisted IPs from environment (comma-separated)
            whitelist = os.environ.get('ADMIN_IP_WHITELIST', '').split(',')
            whitelist = [ip.strip() for ip in whitelist if ip.strip()]
            
            if whitelist:
                client_ip = self.get_client_ip(request)
                if client_ip not in whitelist:
                    logger.warning(f'Unauthorized admin access attempt from {client_ip}')
                    return HttpResponse('Access denied', status=403)
        return None
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

