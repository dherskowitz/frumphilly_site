# Generated by Django 3.1.3 on 2021-01-28 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_auto_20210128_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='activated_at',
            field=models.DateTimeField(default=None),
        ),
    ]