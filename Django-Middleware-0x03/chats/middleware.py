# chats/middleware.py
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        path = request.path
        timestamp = datetime.now()
        log_entry = f"{timestamp} - User: {user} - Path: {path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Deny access outside 18:00 (6 PM) to 21:00 (9 PM)
        if not (18 <= current_hour < 21):
            # Optional: only restrict access to chat URLs
            if request.path.startswith('/chats'):
                return HttpResponseForbidden("Access to chats is only allowed between 6PM and 9PM.")

        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store timestamps of POSTs per IP
        self.message_log = defaultdict(list)

    def __call__(self, request):
        # Only track chat POSTs
        if request.method == 'POST' and request.path.startswith('/chats'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Remove messages older than 1 minute
            self.message_log[ip] = [
                ts for ts in self.message_log[ip]
                if now - ts < timedelta(minutes=1)
            ]

            if len(self.message_log[ip]) >= 5:
                return HttpResponseForbidden("Too many messages. Try again in a minute.")

            self.message_log[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Handle reverse proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to /chats/ actions
        if request.path.startswith('/chats'):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            # Check for role attribute on user
            user_role = getattr(user, 'role', None)

            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        return self.get_response(request)