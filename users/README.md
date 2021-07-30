# Custom User model with UUID as ID and soft delete  

## Installation

Add 'users' to your installed apps in 'your_project_name'/settings.py 

example:

    INSTALLED_APPS = [
        'users',
        ...
    ]

Add this line somewhere in your 'your_project_name'/settings.py file :

    AUTH_USER_MODEL = 'users.User'

To your urls.py add :

    from users.controllers.UserViewSet import UserViewSet

    router = routers.DefaultRouter()
    router.register(r'users', UserViewSet)

To urlpatterns add rest framework router ( if you haven't done this before):

    urlpatterns = [
        path('endpoint_name/', include(router.urls)),
    ]



###Migrate Database:
    python manage.py migrate users

###Create Super User(Admin)
Likely you will need to set admin data :

    python manage.py createsuperuser

