# Generated by Django 3.1.12 on 2021-08-24 08:59

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0006_auto_20210824_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumpost',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=30000, unique=True),
        ),
    ]
