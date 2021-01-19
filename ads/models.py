import random
import uuid
from datetime import datetime, timedelta
from django.db.models.fields.related import ForeignKey
from django.shortcuts import redirect
from app.storage_backends import S3AdsMediaStorage
from django.db import models
from django.conf import settings
from django.db.models.aggregates import Count


class Ad(models.Model):
    # length stored as days
    ONE_WEEK = 7
    TWO_WEEKS = 14
    ONE_MONTH = 30
    TWO_MONTHS = 60
    THREE_MONTHS = 90
    STATUS_CHOICES = [
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("paused", "Paused"),
        ("review", "In Review"),
    ]
    TYPE_CHOICES = [
        ("sidebar", "Sidebar"),
        ("banner", "Banner"),
    ]
    TERM_CHOICES = [
        (ONE_WEEK, "One Week"),
        (TWO_WEEKS, "Two Weeks"),
        (ONE_MONTH, "One Month"),
        (TWO_MONTHS, "Two Months"),
        (THREE_MONTHS, "Three Months"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="ads",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    title = models.CharField(
        default="",
        max_length=200,
        blank=False,
        help_text="What is the name of this ad for your reference? This will not appear on the site.",
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, blank=False, default="inactive"
    )
    type = models.CharField(
        max_length=50, choices=TYPE_CHOICES, blank=False, default="inactive", verbose_name="Type of Ad"
    )
    image = models.ImageField(
        storage=S3AdsMediaStorage(),
        default=None,
        help_text="Upload an image for your ad in either jpg/png/gif format. Dimensions should be 300x250.",
        null=True,
        blank=True,
    )
    contract_length = models.IntegerField(
        default=ONE_WEEK,
        choices=TERM_CHOICES,
        help_text="Amount of times the ad will be active for.",
    )
    redirect_to = models.URLField(
        default=None,
        verbose_name="Send Ad To",
        help_text="Enter the URL where the ad should be linked to. (Must include http:// or https://)",
    )
    redirect_uuid = models.CharField(max_length=100, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ad"
        verbose_name_plural = "ads"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.redirect_uuid = str(uuid.uuid4()).split('-')[-1]
        super().save(*args, **kwargs)

    def mark_expired():
        ads = Ad.objects.filter(status='active')
        for ad in ads:
            expires_at = ad.created_at + timedelta(days=ad.contract_length)
            if datetime.now() > expires_at.replace(tzinfo=None):
                ad.status = 'expired'
                ad.save()

    def get_sidebar_ads():
        # https://stackoverflow.com/a/32389679
        all_ads = Ad.objects.filter(status='active', type='sidebar').values_list('id', flat=True)
        random_ads = random.sample(list(all_ads), min(len(all_ads), 2))
        if random_ads:
            ads_qset = Ad.objects.filter(id__in=random_ads)
            ads_list = list(ads_qset)
            random.shuffle(ads_list)
            return ads_list

    def get_banner_ad():
        # https://stackoverflow.com/a/2118712
        count = Ad.objects.filter(status='active', type='banner').aggregate(count=Count('id'))['count']
        if count:
            random_index = random.randint(0, count - 1)
            return Ad.objects.filter(status='active', type='banner').all()[random_index]

    def get_active_ads():
        Ad.mark_expired()
        return {
            'sidebar_ads': Ad.get_sidebar_ads(),
            'banner_ad': Ad.get_banner_ad(),
        }

    def time_remaining(self):
        if self.status == 'active':
            expires_at = self.created_at + timedelta(days=self.contract_length)
            remaining = expires_at.replace(tzinfo=None) - datetime.now()
            return remaining.days
        elif self.status == 'expired':
            expired_at = self.created_at - timedelta(days=self.contract_length)
            remaining = datetime.now() - expired_at.replace(tzinfo=None)
            return expired_at
        else:
            return ''
