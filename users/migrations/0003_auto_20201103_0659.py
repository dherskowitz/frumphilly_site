# Generated by Django 3.1.3 on 2020-11-03 11:59

import app.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_avatar'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='avatar',
            new_name='_avatar',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='_avatar',
            field=models.ImageField(blank=True, db_column='avatar', default=None, help_text='Upload an image for your avatar.', null=True, storage=app.storage_backends.S3UserAccountStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
