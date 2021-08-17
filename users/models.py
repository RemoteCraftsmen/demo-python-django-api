"""
Custom User Model with UUID and mail as username
"""
from datetime import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import make_aware

from safedelete.models import SafeDeleteModel, SOFT_DELETE


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, SafeDeleteModel):
    """
    Custom User model with UUID as ID, email as username, soft delete, and password reset fields
    """
    _safedelete_policy = SOFT_DELETE

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    passwordResetToken = models.CharField(null=True, max_length=200)
    passwordResetTokenExpiresAt = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def is_password_reset_token_expired(self):
        """
        Checks if password reset token expired
        """
        return (self.passwordResetTokenExpiresAt is None) \
               or \
               (make_aware(datetime.now()) > self.passwordResetTokenExpiresAt)

    def __str__(self):
        return self.email

    class Meta:
        """
        Meta data for user model
        https://docs.djangoproject.com/en/3.2/ref/models/options/
        """
        db_table = 'auth_user'

    objects = UserManager()
