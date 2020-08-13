from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(default="", blank=False, max_length=50)
    slug = models.SlugField(default="", blank=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # if not self.slug:
        self.slug = slugify(f"{self.title}")
        super().save(*args, **kwargs)

    def get_category_by_slug(slug):
        return Category.objects.filter(slug=slug)


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
        if not self.slug:
            self.slug = slugify(f"{self.business_name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/listings/{self.slug}"

    def get_listings():
        return Listing.objects.all()

    def get_listings_by_category(slug):
        return Listing.objects.filter(categories__slug=slug)