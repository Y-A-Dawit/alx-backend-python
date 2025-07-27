# messaging_app/chats/auth.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomJWTAuthentication(JWTAuthentication):
    """
    Optional customization of JWT authentication.
    Extend this class if you want to:
    - Add logging
    - Reject inactive users
    - Support additional headers or tokens
    """
    
    def authenticate(self, request):
        # Call the base implementation
        auth_result = super().authenticate(request)

        if auth_result is None:
            return None

        user, validated_token = auth_result

        # Example: reject inactive users
        if not user.is_active:
            raise AuthenticationFailed('User account is inactive.')

        # Add more custom checks here if needed

        return user, validated_token
