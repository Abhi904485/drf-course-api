from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomCookieAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the custom key from cookies
        custom_value = request.COOKIES.get("my_custom_key")

        if custom_value != "my_custom_value":
            raise AuthenticationFailed("Invalid authentication cookie")
