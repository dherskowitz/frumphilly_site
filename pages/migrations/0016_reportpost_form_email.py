# Generated by Django 3.1.13 on 2021-12-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_auto_20211222_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportpost',
            name='form_email',
            field=models.EmailField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
