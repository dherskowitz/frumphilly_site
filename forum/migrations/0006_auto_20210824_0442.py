# Generated by Django 3.1.12 on 2021-08-24 08:42

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20210824_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumthread',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=50000, unique=True),
        ),
    ]