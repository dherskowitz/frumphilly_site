from django.db import models


class ForumCategory(models.Model):
    pass


class ForumThread(models.Model):
    # Thread belongs to a category
    pass


class ForumPost(models.Model):
    # Post goes in a thread
    pass
