# Generated by Django 3.0.2 on 2020-09-03 14:03

import app.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_listing_cover_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('description', models.TextField(blank=True, default='')),
                ('slug', models.SlugField(blank=True, default='')),
                ('image', models.ImageField(blank=True, default=None, null=True, storage=app.storage_backends.S3SiteImagesStorage(), upload_to='')),
            ],
            options={
                'verbose_name': 'listing type',
                'verbose_name_plural': 'listing types',
            },
        ),
    ]
