# Generated by Django 3.1.3 on 2020-12-07 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20201206_0819'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='neighborhood',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
    ]