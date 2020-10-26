import utils
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from itertools import chain
from app.storage_backends import S3ListingsMediaStorage, S3SiteImagesStorage


class CategoryGroup(models.Model):
    title = models.CharField(default="", blank=False, max_length=50)
    description = models.TextField(default="", blank=True)
    slug = models.SlugField(default="", blank=True)
    image = models.ImageField(
        storage=S3SiteImagesStorage(), default=None, null=True, blank=True,
    )

    class Meta:
        verbose_name = "category group"
        verbose_name_plural = "category groups"

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
    slug = models.SlugField(default="", blank=True)
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
        help_text="Enter the URL of your website if you have one.",
    )
    facebook = models.URLField(
        default="",
        null=True,
        blank=True,
        help_text="Enter the URL of your Facebook page if you have one.",
    )
    twitter = models.URLField(
        default="",
        null=True,
        blank=True,
        help_text="Enter the URL of your Twitter page if you have one.",
    )
    instagram = models.URLField(
        default="",
        null=True,
        blank=True,
        help_text="Enter the URL of your Instagram page if you have one.",
    )
    phone = models.CharField(
        max_length=18,
        default=None,
        null=True,
        blank=True,
        help_text="Enter your Phone number.",
    )
    fax = models.CharField(
        max_length=18,
        default=None,
        null=True,
        blank=True,
        help_text="Enter your Fax number.",
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
        help_text="If you are a food business what Kashrut do you have.",
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
    slug = models.SlugField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

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
        return f"/listings/{self.slug}"

    def get_listings():
        return Listing.objects.all()

    def get_listings_by_category_or_group(slug):
        is_category = Category.objects.filter(slug=slug).exists()
        is_category_group = CategoryGroup.objects.filter(slug=slug).exists()

        if is_category:
            listings = Listing.objects.filter(categories__slug=slug).distinct(
                "business_name"
            )
        if is_category_group:
            listings = Listing.objects.filter(
                categories__category_group__slug=slug
            ).distinct("business_name")
        return listings

    def filter_by_city(city):
        return Listing.objects.filter(city__icontains=city).order_by("-business_name")

    def get_cities():
        return Listing.objects.order_by("city").values("city").distinct()
