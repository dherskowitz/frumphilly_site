from django.db import models
from django.conf import settings
from app.storage_backends import EventMediaStorage, EventFileStorage


# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_name = models.CharField(
        default="", max_length=150, help_text="What is the name of this event?"
    )
    event_host = models.CharField(
        default="",
        max_length=250,
        help_text="What organisation is hosting this event?",
        blank=True,
    )
    event_image = models.FileField(
        storage=EventMediaStorage(),
        default=None,
        help_text="Upload an image or poster for this event.",
        blank=True,
    )
    event_attachment = models.FileField(
        storage=EventFileStorage(),
        default=None,
        help_text="Upload a PDF file.",
        blank=True,
    )
    event_link = models.URLField(
        default=None,
        max_length=200,
        blank=True,
        help_text="Add a link to your website or the event webpage here.",
    )
    event_location = models.CharField(
        max_length=500, default=None, help_text="Where will this event take place?"
    )
    event_description = models.TextField(
        blank=True,
        help_text="Here is where you can talk about your event in greater detail.",
    )
    event_email_contact = models.EmailField(
        max_length=254,
        default=None,
        blank=True,
        help_text="Where can people email with any questions?",
    )
    event_phone_contact = models.CharField(
        max_length=18,
        default=None,
        help_text="Where can people call with any questions?",
        blank=True,
    )
    event_video = models.URLField(
        max_length=300,
        default=None,
        help_text="Include a video about your event.",
        blank=True,
    )
    event_start_time = models.TimeField(
        default=None, auto_now=False, auto_now_add=False, blank=True
    )
    event_start_date = models.DateField(
        default=None, auto_now=False, auto_now_add=False
    )
    event_end_date = models.DateField(
        default=None, auto_now=False, auto_now_add=False, blank=True
    )
    event_rsvp = models.BooleanField(
        default=None, help_text="Does your event require RSVP or tickets?"
    )
    event_cost = models.DecimalField(default=None, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.event_name
