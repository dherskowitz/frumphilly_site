# Generated by Django 3.0.2 on 2020-07-19 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='slug',
            field=models.SlugField(blank=True, default=''),
        ),
    ]
