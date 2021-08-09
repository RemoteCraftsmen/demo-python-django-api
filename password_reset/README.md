# Password Reset for Django

## Installation

Add `password_reset` to your installed apps in `your_project_name/settings.py` 

example:

    INSTALLED_APPS = [
        'password_reset',
        ...
    ]

To your `urls.py` add :

    from password_reset.routes.reset_password import urls as password_reset_routes


    urlpatterns = [
       path('auth/', include(password_reset_routes)),
    ]

Add your mail settings (port,username ect) to your setting.py.


##Endpoints
In your app 2 new endpoints will appear :
    
    auth/password-reset  (for generate password token)
    auth/password-reset/<str:token> (for using token)

##User model
User model should have 2 extra fields:

    passwordResetToken = models.CharField(null=True, max_length=200)
    passwordResetTokenExpiresAt = models.DateTimeField(null=True)

