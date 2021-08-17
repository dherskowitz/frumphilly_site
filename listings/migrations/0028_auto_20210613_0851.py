# Generated by Django 3.1.8 on 2021-06-13 12:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('listings', '0027_auto_20210613_0729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='likes',
        ),
        migrations.AddField(
            model_name='listing',
            name='likes',
            field=models.ManyToManyField(related_name='listing_like', to=settings.AUTH_USER_MODEL),
        ),
    ]