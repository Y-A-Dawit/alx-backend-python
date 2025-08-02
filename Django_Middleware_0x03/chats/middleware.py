# chats/middleware.py
from datetime import datetime
from django.http import HttpResponseForbidden

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
