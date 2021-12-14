import utils
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from itertools import chain
from app.storage_backends import S3ListingsMediaStorage, S3SiteImagesStorage


class CategoryGroup(models.Model):
    title = models.CharField(default="", blank=False, max_length=50)
    description = models.TextField(default="", blank=True)
    slug = models.SlugField(default="", blank=True, max_length=255)
    image = models.ImageField(
        storage=S3SiteImagesStorage(), default=None, null=True, blank=True,
    )

    class Meta:
        verbose_name = "Category Group"
        verbose_name_plural = "Category Groups"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image:
            # call the compress function
            new_image = utils.compress(self.image)
            # set self.image to new_image
            self.image = new_image
            # save
            super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_all_listing_types():
        return CategoryGroup.objects.all().order_by('title')


class Category(models.Model):
    title = models.CharField(default="", blank=False, max_length=50)
    slug = models.SlugField(default="", blank=True, max_length=255)
    category_group = models.ForeignKey(
        CategoryGroup, on_delete=models.SET_NULL, null=True
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_category_or_group(slug):
        category_single = Category.objects.filter(slug=slug)
        category_group = CategoryGroup.objects.filter(slug=slug)
        category = sorted(
            chain(category_single, category_group),
            key=lambda category: category.slug,
            reverse=True,
        )
        return category


class Listing(models.Model):
    STATUS_CHOICES = [
        ("draft", "Save for Later"),
        ("published", "Published"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="listings",
    )
    business_name = models.CharField(
        default="",
        max_length=200,
        blank=False,
        help_text="What is the name of this business?",
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, blank=False, default="published",
        help_text="Only Published listings are publicly visible.",
    )
    cover_image = models.ImageField(
        storage=S3ListingsMediaStorage(),
        default=None,
        help_text="Upload a cover image for your listing.",
        null=True,
        blank=True,
    )
    website = models.URLField(
        default="",
        null=True,
        blank=True,
        help_text="Enter the URL of your website if you have one. (Must include http:// or https://)",
    )
    facebook = models.URLField(
        default="",
        null=True,
        blank=True,
        help_text="Enter the URL of your Facebook page if you have one. (Must include http:// or https://)",
    )
    twitter = models.URLField(
        default="",
        null=True,
        blank=True,
        help_text="Enter the URL of your Twitter page if you have one. (Must include http:// or https://)",
    )
    instagram = models.URLField(
        default="",
        null=True,
        blank=True,
        help_text="Enter the URL of your Instagram page if you have one. (Must include http:// or https://)",
    )
    phone = models.CharField(
        max_length=18,
        default=None,
        null=True,
        blank=True,
        help_text="Enter your Phone number.",
    )
    mobile = models.CharField(
        max_length=18,
        default=None,
        null=True,
        blank=True,
        help_text="Enter your mobile number.",
    )
    whatsapp = models.CharField(
        max_length=18,
        default=None,
        null=True,
        blank=True,
        help_text="Enter your WhatsApp number if you have one.",
    )
    email = models.EmailField(
        max_length=254,
        default=None,
        null=True,
        blank=True,
        help_text="Enter your email address if you have one.",
    )
    location = models.CharField(
        max_length=500, blank=False, help_text="Enter the Address of your business",
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
    summary = models.CharField(
        max_length=120,
        default=None,
        null=True,
        blank=True,
        help_text="120 character description of your business",
    )
    description = models.TextField(
        default=None,
        null=True,
        blank=True,
        help_text="Full description of your business",
    )
    kashrut = models.CharField(
        max_length=120,
        default=None,
        null=True,
        blank=True,
        help_text="What Kashrut do you have.",
    )
    sun_thu_hours = models.CharField(
        max_length=120,
        default=None,
        null=True,
        blank=True,
        help_text="What are your hours Sun-Thurs.",
    )
    friday_hours = models.CharField(
        max_length=120,
        default=None,
        null=True,
        blank=True,
        help_text="What are your hours on Friday.",
    )
    saturday_hours = models.CharField(
        max_length=120,
        default=None,
        null=True,
        blank=True,
        help_text="What are your hours Saturday (if any).",
    )
    claimed = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    accept_cc = models.BooleanField(default=False)
    delivers = models.BooleanField(default=False)
    wheelchair_access = models.BooleanField(default=False)
    slug = models.SlugField(default="", blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    likes = GenericRelation('ListingLike', related_query_name='likes')

    class Meta:
        verbose_name = "listing"
        verbose_name_plural = "listings"

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        if self.cover_image:
            # call the compress function
            new_image = utils.compress(self.cover_image)
            # set self.image to new_image
            self.cover_image = new_image
            # save
            super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.business_name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/listings/{self.slug}-{self.id}"

    def get_listings():
        return Listing.objects.filter(status="published")

    def get_listings_by_group(slug):
        return Listing.objects.filter(
            categories__category_group__slug=slug,
            status="published"
        ).distinct("business_name")

    def filter_by_city(city):
        return Listing.objects.filter(city__icontains=city).order_by("-business_name")

    def get_cities():
        return Listing.objects.order_by("city").values("city").distinct()

    def likes_count(self):
        return self.likes.count()

    def like(self, user):
        return self.likes.create(user=user)

    def dislike(self, user):
        return self.likes.filter(user=user).delete()

    def is_liked_by(self, user):
        liked_list = self.likes.values_list('user__id', flat=True)
        return user.id in liked_list


class ListingLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self):
        listing = Listing.objects.get(id=self.object_id)
        return f"{self.user.email} liked {listing.business_name}"
