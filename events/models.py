from django.db import models
from django.conf import settings
from app.storage_backends import EventMediaStorage, EventFileStorage
from datetime import date


# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(
        default="", max_length=150, help_text="What is the name of this event?"
    )
    host = models.CharField(
        default="",
        max_length=250,
        help_text="What organisation is hosting this event?",
        null=True,
        blank=True,
    )
    image = models.FileField(
        storage=EventMediaStorage(),
        default=None,
        help_text="Upload an image or poster for this event.",
        null=True,
        blank=True,
    )
    attachment = models.FileField(
        storage=EventFileStorage(),
        default=None,
        help_text="Upload a PDF file.",
        null=True,
        blank=True,
    )
    link = models.URLField(
        default=None,
        max_length=200,
        null=True,
        blank=True,
        help_text="Add a link to your website or the event webpage here.",
    )
    location = models.CharField(
        max_length=500, default=None, help_text="Where will this event take place?"
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Here is where you can talk about your event in greater detail.",
    )
    email_contact = models.EmailField(
        max_length=254,
        default=None,
        null=True,
        blank=True,
        help_text="Where can people email with any questions?",
    )
    phone_contact = models.CharField(
        max_length=18,
        default=None,
        help_text="Where can people call with any questions?",
        null=True,
        blank=True,
    )
    video = models.URLField(
        max_length=300,
        default=None,
        help_text="Include a video about your event.",
        null=True,
        blank=True,
    )
    start_time = models.TimeField(
        default=None, auto_now=False, auto_now_add=False, null=True, blank=True
    )
    start_date = models.DateField(default=None, auto_now=False, auto_now_add=False)
    end_date = models.DateField(
        default=None, auto_now=False, auto_now_add=False, null=True, blank=True
    )
    rsvp = models.BooleanField(
        default=None, help_text="Does your event require RSVP or tickets?"
    )
    cost = models.DecimalField(
        default=None, max_digits=8, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return self.name

    @property
    def event_in_past(self):
        return date.today() > self.start_date
