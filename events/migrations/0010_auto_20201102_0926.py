# Generated by Django 3.0.2 on 2020-11-02 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20200917_0235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'verbose_name': 'Event Category', 'verbose_name_plural': 'Event Categories'},
        ),
    ]
