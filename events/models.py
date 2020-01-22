from django.db import models
from django.conf import settings


# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
