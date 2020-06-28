import re
import requests
from io import BytesIO
from PIL import Image
from uuid import uuid4
from decouple import config
from django.core.files import File
from django.db import models
from django.conf import settings
from app.storage_backends import S3EventsMediaStorage, S3EventsFileStorage
from datetime import date, datetime, timedelta
from django.utils.text import slugify


def compress(image):
    """"Compress submitted images"""
    size = 600, 600
    im = Image.open(image)
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(im_io, "JPEG", quality=70)
    # create a django-friendly Files object
    new_image = File(im_io, name=image.name)
    return new_image


def get_video(video_link):
    """Parse submitted data for video id or iFrame src and normalize url"""
    video = video_id = ""
    if re.search("iframe", video_link):
        """If video is iFrame grab src and set as video"""
        source = re.findall('src\s*=\s*"(.+?)"', video_link)
        if len(source) > 0:
            video = source[0]
    elif re.search("youtube", video_link) or re.search("youtu.be", video_link):
        """If video is youtube link get video id and build url for video"""
        if re.search("youtube.com/watch", video_link):
            video_id = video_link.split("v=")[1]
            if re.search("&", video_link):
                temp = video_link.split("&")[0]
                video_id = temp.split("v=")[-1]
        elif re.search("youtu.be", video_link) or re.search(
            "youtube.com/embed", video_link
        ):
            video_id = video_link.split("/")[-1]
        video = f"https://youtube.com/embed/{video_id}"
    elif re.search("vimeo", video_link):
        """If video is vimeo link get video id and build url for video"""
        video_id = video_link.split("/")[-1]
        video = f"https://player.vimeo.com/video/{video_id}"
    return video


# Create your models here.
class Event(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="events",
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
        storage=S3EventsMediaStorage(),
        default=None,
        help_text="Upload an image or poster for this event.",
        null=True,
        blank=True,
    )
    attachment = models.FileField(
        storage=S3EventsFileStorage(),
        default=None,
        help_text="Upload a PDF file with more details.",
        null=True,
        blank=True,
    )
    link = models.URLField(
        default=None,
        max_length=200,
        null=True,
        blank=True,
        help_text="A link to your website or event webpage.",
    )
    location = models.CharField(
        max_length=500,
        default=None,
        help_text="Address where this event take place...",
    )
    suburb = models.CharField(
        max_length=500, default=None, null=True, blank=True, help_text="",
    )
    city = models.CharField(
        max_length=500, default=None, null=True, blank=True, help_text="",
    )
    state = models.CharField(
        max_length=500, default=None, null=True, blank=True, help_text="",
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
        verbose_name="Email Contact",
        help_text="Where can people email with any questions?",
    )
    phone_contact = models.CharField(
        max_length=18,
        default=None,
        help_text="Where can people call with any questions?",
        verbose_name="Phone Contact",
        null=True,
        blank=True,
    )
    video = models.CharField(
        max_length=300,
        default=None,
        help_text="Add a link to a youtube/vimeo video.",
        null=True,
        blank=True,
    )
    start_time = models.TimeField(
        default=None,
        auto_now=False,
        auto_now_add=False,
        verbose_name="Start Time",
        null=True,
        blank=True,
        help_text="HOUR:MINUTE:AM/PM",
    )
    start_date = models.DateField(
        default=None,
        auto_now=False,
        auto_now_add=False,
        verbose_name="Start Date",
        help_text="When will your event take place?",
    )
    end_date = models.DateField(
        default=None,
        auto_now=False,
        auto_now_add=False,
        verbose_name="End Date",
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
        help_text="Numbers only, currency symbol will not work.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.location:
            base_url = "https://api.geocod.io/v1.6/geocode"
            api_key = config("GEOCODING_KEY")
            req = requests.get(f"{base_url}?q={self.location}&api_key={api_key}")
            data = req.json()
            self.suburb = data["results"][0]["address_components"]["county"]
            self.city = data["results"][0]["address_components"]["city"]
            self.state = data["results"][0]["address_components"]["state"]
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
        if not self.slug:
            self.slug = slugify(f"{self.name} {my_id}")
        if self.video is not None:
            self.video = get_video(self.video)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/events/{self.slug}"

    @property
    def event_in_past(self):
        return date.today() > self.start_date

    def get_upcoming_events():
        today = datetime.today()
        future_timedelta = timedelta(days=30)
        future_date = today + future_timedelta
        events = (
            Event.objects.filter(start_date__lte=future_date)
            .filter(start_date__gte=today)
            .order_by("start_date")
        )
        return events
