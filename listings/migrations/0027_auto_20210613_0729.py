# Generated by Django 3.1.8 on 2021-06-13 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0026_listing_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='likes',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]