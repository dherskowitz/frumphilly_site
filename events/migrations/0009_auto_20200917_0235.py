# Generated by Django 3.0.2 on 2020-09-17 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20200917_0234'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventsCategory',
            new_name='EventCategory',
        ),
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'verbose_name': 'event category', 'verbose_name_plural': 'event categories'},
        ),
    ]