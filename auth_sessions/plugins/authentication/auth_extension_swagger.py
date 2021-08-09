from drf_spectacular.extensions import OpenApiAuthenticationExtension
from auth_sessions.plugins.authentication.CsrfExemptSessionAuthentication import CsrfExemptSessionAuthentication


class CustomSessionScheme(OpenApiAuthenticationExtension):
    name = "cookieAuth"
    target_class = CsrfExemptSessionAuthentication
    priority = -1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'sessionid',
        }
