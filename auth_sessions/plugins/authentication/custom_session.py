"""
Custom Sessions-Authentication classes
"""
from rest_framework import authentication


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    """
    Doesn't use CSFR token, therefore it solves problems with using sessions with API
    """
    def enforce_csrf(self, request):
        return
