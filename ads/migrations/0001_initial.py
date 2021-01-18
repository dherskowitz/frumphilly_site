# Generated by Django 3.1.3 on 2021-01-18 12:23

import app.storage_backends
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', help_text='What is the name of this ad? Use the company/listing name plus a descriptor.', max_length=200)),
                ('status', models.CharField(choices=[('inactive', 'Inactive'), ('active', 'Active'), ('expired', 'Expired'), ('paused', 'Paused'), ('review', 'In Review')], default='inactive', max_length=50)),
                ('type', models.CharField(choices=[('sidebar', 'Sidebar'), ('banner', 'Banner')], default='inactive', max_length=50)),
                ('image', models.ImageField(blank=True, default=None, help_text='Upload an image for your ad.', null=True, storage=app.storage_backends.S3AdsMediaStorage(), upload_to='')),
                ('contract_length', models.IntegerField(choices=[(1, 'One Week'), (2, 'Two Weeks'), (4, 'One Month'), (8, 'Two Months'), (12, 'Three Months')], default=1, help_text='Amount of times the ad will be active for.')),
                ('redirect_to', models.URLField(default=None, help_text='Enter the URL where the ad should be linked to. (Must include http:// or https://)')),
                ('redirect_uuid', models.CharField(default=None, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ad',
                'verbose_name_plural': 'ads',
            },
        ),
    ]
