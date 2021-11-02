from django.conf import settings
from django.db import models
from django.utils.text import slugify
from app.storage_backends import S3SiteImagesStorage
from uuid import uuid4


class ForumCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    description = models.CharField(max_length=300, blank=True, null=True)
    icon = models.ImageField(storage=S3SiteImagesStorage(), default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/forum/{self.slug}"

    def get_thread_count(self):
        return ForumThread.objects.filter(category__slug=self.slug).count()

    def get_post_count(self):
        return ForumPost.objects.filter(thread__category__slug=self.slug).count()

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=150, unique=True, editable=False)
    content = models.TextField(max_length=50000, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/forum/{self.category.slug}/{self.slug}"

    def get_post_count(self):
        return ForumPost.objects.filter(thread__slug=self.slug).count()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title + "-" + uuid4().hex[-8:])
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = "Threads"


class ForumPost(models.Model):
    # Post goes in a thread
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=30000, blank=False, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.email} replied to {self.thread.title} at {self.created_at}"

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = "Posts"
