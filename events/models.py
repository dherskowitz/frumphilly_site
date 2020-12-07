import utils
from uuid import uuid4
from django.utils.text import slugify
from django.db import models
from django.conf import settings
from app.storage_backends import S3EventsMediaStorage, S3EventsFileStorage
from datetime import date, datetime, timedelta


class EventCategory(models.Model):
    title = models.CharField(default="", max_length=50)
    slug = models.SlugField(default="", blank=True)

    class Meta:
        verbose_name = "Event Category"
        verbose_name_plural = "Event Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)


class Event(models.Model):
    STATUS_CHOICES = [
        ("draft", "Save for Later"),
        ("published", "Published"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="events",
    )
    name = models.CharField(
        default="", max_length=150, help_text="What is the name of this event?"
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, blank=False, default="draft",
        help_text="Events will not show until Published",
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
    is_virtual_event = models.BooleanField(
        default=False,
        help_text="Check this box if this is an online only event.",
        verbose_name="Virtual Event",
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
        null=True,
        blank=True,
        help_text="Address where this event take place...",
    )
    neighborhood = models.CharField(
        max_length=500, default=None, null=True, blank=True, help_text="",
    )
    city = models.CharField(
        max_length=500, default=None, null=True, blank=True, help_text="",
    )
    state = models.CharField(
        max_length=500, default=None, null=True, blank=True, help_text="",
    )
    zipcode = models.CharField(
        max_length=500, default=None, null=True, blank=True, help_text="",
    )
    location_type = models.CharField(
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
    categories = models.ManyToManyField(EventCategory)

    class Meta:
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            # call the compress function
            new_image = utils.compress(self.image)
            # set self.image to new_image
            self.image = new_image
            # save
            super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify({self.name})
        if self.video is not None:
            self.video = utils.get_video(self.video)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/events/{self.slug}-{self.id}"

    @property
    def event_in_past(self):
        return date.today() > self.start_date

    def get_upcoming_events():
        today = datetime.today()
        future_timedelta = timedelta(days=30)
        future_date = today + future_timedelta
        events = (
            Event.objects.filter(start_date__lte=future_date)
            .filter(start_date__gte=today, status="published")
            .order_by("start_date")
        )
        return events

    def get_cities():
        return Event.objects.order_by("city").values("city").distinct()

    def get_categories():
        return EventCategory.objects.order_by("title").values("title", "slug").distinct()

    def get_events_by_category(slug):
        return Event.objects.filter(categories__slug=slug, status="published")

    def get_events_by_city(city):
        return Event.objects.filter(city__iexact=city)
