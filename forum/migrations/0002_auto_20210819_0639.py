# Generated by Django 3.1.12 on 2021-08-19 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forumpost',
            old_name='title',
            new_name='thread',
        ),
    ]