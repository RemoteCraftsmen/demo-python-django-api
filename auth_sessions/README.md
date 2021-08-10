# Session authentication
## for Django Rest Framework

## Installation

Add `auth_sessions` to your installed apps in `your_project_name/settings.py` 

example:

```
INSTALLED_APPS = [
    'auth_sessions',
]
```

Add this line somewhere in your `your_project_name/settings.py` file :

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'auth_sessions.plugins.authentication.CsrfExemptSessionAuthentication.CsrfExemptSessionAuthentication',
    ],
}
```

To your `urls.py` add :

```
from auth_sessions.plugins.error_handlers import no_found_error_handle
from auth_sessions.routes import urlpatterns as auth_sessions_routes
```

At end of `urls.py` add:

```
handler404 = no_found_error_handle
```

In the same file add new routes to urlpatterns :

```    
urlpatterns = [
    path('api/', include(auth_sessions_routes)),
]
```

### For Swagger (drf_spectacular)
Create file `__init__.py` in your app dir (the dir where you got models,migrations,test)
Add this line:

```
from auth_sessions.plugins.authentication.auth_extension_swagger import CsrfExemptSessionAuthentication
```