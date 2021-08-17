"""
Authentication classes for Swagger/Spectacular
"""
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from auth_sessions.plugins.authentication.custom_session \
    import CsrfExemptSessionAuthentication


class CustomSessionScheme(OpenApiAuthenticationExtension):
    """
    Custom session authentication without CSFR
    """
    name = "cookieAuth"
    target_class = CsrfExemptSessionAuthentication
    priority = -1

    def get_security_definition(self, auto_schema):
        """
        Returns security settings for swagger
        """
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'sessionid',
        }
