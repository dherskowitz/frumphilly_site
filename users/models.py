from app.storage_backends import S3UserAccountStorage
from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import User
from django.db import models
from events.models import Event
from listings.models import Listing
from ads.models import Ad


# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here
    _avatar = models.ImageField(
        storage=S3UserAccountStorage(),
        default=None,
        help_text="Upload an image for your avatar.",
        null=True,
        blank=True,
        db_column='avatar'
    )

    @property
    def avatar(self):
        return self._avatar

    @avatar.setter
    def avatar(self, value):
        self._avatar = value

    def __str__(self):
        return self.email

    def get_user_settings(user):
        return CustomUser.objects.filter(id=user.id).first()

    def get_events_count(request):
        return Event.objects.filter(created_by=request.user).count()

    def get_listings_count(request):
        return Listing.objects.filter(created_by=request.user).count()

    def get_ads_count(request):
        return Ad.objects.filter(user=request.user).count()
