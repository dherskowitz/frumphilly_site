# Generated by Django 3.0.2 on 2020-08-10 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_listing_delivers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='categories',
            field=models.ManyToManyField(error_messages={'required': 'Please select at least one category!'}, to='listings.Category'),
        ),
    ]
