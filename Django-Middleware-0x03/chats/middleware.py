import logging
import time
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, JsonResponse
from collections import defaultdict

logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('requests.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username
        
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access denied: You can only access the chat between 6 AM and 9 PM.")

        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware:
    """
    Middleware that tracks number of POST requests (messages) from each IP address
    and enforces a limit of 5 messages per 1-minute window.
    """
    # Dictionary to store requests per IP: {ip: [timestamps]}
    ip_request_times = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only count POST requests (sending messages)
        if request.method == "POST" and request.path.startswith("/chat/"):  # adjust path as needed
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Remove timestamps older than 1 minute
            self.ip_request_times[ip] = [
                timestamp for timestamp in self.ip_request_times[ip]
                if current_time - timestamp < 60
            ]

            # Check if limit exceeded
            if len(self.ip_request_times[ip]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded: Maximum 5 messages per minute."},
                    status=429
                )

            # Add current request timestamp
            self.ip_request_times[ip].append(current_time)

        # Continue processing the request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Get the client IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolePermissionMiddleware:
    """
    Middleware to restrict access based on user roles.
    Only 'admin' and 'moderator' users are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            if user.role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: Insufficient permissions.")
        else:
            return HttpResponseForbidden("Access denied: Authentication required.")

     
        response = self.get_response(request)
        return response
