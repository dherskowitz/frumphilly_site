from io import BytesIO
from PIL import Image
from uuid import uuid4
from django.core.files import File
from django.db import models
from django.conf import settings
from app.storage_backends import EventMediaStorage, EventFileStorage
from datetime import date
from django.utils.text import slugify
from django.urls import reverse


def compress(image):
    size = 800, 800
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(im_io, "JPEG", quality=70)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(
        default="", max_length=150, help_text="What is the name of this event?"
    )
    slug = models.SlugField(default="",)
    host = models.CharField(
        default="",
        max_length=250,
        help_text="What organisation is hosting this event?",
        null=True,
        blank=True,
    )
    image = models.ImageField(
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
        default=None,
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        help_text="What time does your event start?",
    )
    start_date = models.DateField(
        default=None,
        auto_now=False,
        auto_now_add=False,
        help_text="When will your event take place?",
    )
    end_date = models.DateField(
        default=None,
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        help_text="If your event occurs over multiple days, when will your event end?",
    )
    rsvp = models.BooleanField(
        default=None,
        help_text="Does your event require RSVP or tickets?",
        verbose_name="RSVP",
    )
    cost = models.DecimalField(
        default=None,
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="If anything, how much will it cost to attend your event?",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            # call the compress function
            new_image = compress(self.image)
            # set self.image to new_image
            self.image = new_image
            # save
            super().save(*args, **kwargs)
        # Generate UUID4 and take the last segment for unique slug
        my_uuid = uuid4()
        my_id = str(my_uuid).rsplit("-")[-1:]
        self.slug = slugify(f"{self.name} {my_id}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/events/{self.slug}/"
        # return reverse('events_single', args=[str(self.slug)])

    @property
    def event_in_past(self):
        return date.today() > self.start_date
