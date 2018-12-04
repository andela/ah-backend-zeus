import jwt

from django.conf import settings

from rest_framework import authentication, exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header)
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        """
        The method splits the token header and
        if successful it returns user/token combination 
        to the _authenticate_credentials method. if not, 
        throws an error.
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None

        bearer = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if bearer.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Authenticates the given credentials received from the authenticate method 
        and if authentication is successful, returns the user and token. 
        if not, throws an error.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'User with this token was not found.'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'User with this token has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)