from rest_framework import authentication
from rest_framework import exceptions

from .models import APIKey


class APIKEYAccess(authentication.BaseAuthentication):
    """
    Authenticate overwrite default method. This is temporally running till OAUTh system is integrated.
    """

    message = 'Invalid or missing API Key.'

    def authenticate(self, request):
        api_key = request.META.get('HTTP_AUTHORIZATION', '')
        exist = APIKey.objects.filter(key=api_key).exists()
        if not exist:
            raise exceptions.AuthenticationFailed(self.message)
        return None

