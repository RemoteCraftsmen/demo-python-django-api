from django.db import models
from django.contrib.auth.models import AbstractUser
from safedelete.models import SafeDeleteModel, SOFT_DELETE
import uuid
#ToDo - improve model as in comments ( swaping mail and username )
#from django.utils.translation import gettext_lazy as _


class User(AbstractUser, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    #username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #email = models.EmailField(_('email address'), unique=True)

    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []

    #def __str__(self):
    #    return self.email

    class Meta:
        db_table = 'auth_user'
