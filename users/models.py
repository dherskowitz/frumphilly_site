from django.contrib.auth.models import AbstractUser
from django.db import models
from events.models import Event
from listings.models import Listing


# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email

    def get_events_count():
        return Event.objects.count()

    def get_listings_count():
        return Listing.objects.count()
