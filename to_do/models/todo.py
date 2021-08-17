import uuid

from django.db import models
from django.conf import settings
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE


class Todo(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(max_length=30)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='todos',
                              on_delete=models.CASCADE)
