import os
from django.db import models
from django.conf import settings
from app.storage_backends import EventMediaStorage
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_image = models.FileField(storage=EventMediaStorage(), default="")
