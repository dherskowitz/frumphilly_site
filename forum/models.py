from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from app.storage_backends import S3SiteImagesStorage


class ForumCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    description = models.CharField(max_length=300)
    icon = models.ImageField(storage=S3SiteImagesStorage(), default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class ForumThread(models.Model):
    # Thread belongs to a category
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name="threads")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, editable=False)
    description = models.TextField(max_length=50000, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("thread", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = "Threads"


class ForumPost(models.Model):
    # Post goes in a thread
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=30000, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = "Posts"
