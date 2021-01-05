# Generated by Django 3.1.3 on 2020-12-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_auto_20201207_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('draft', 'Save for Later'), ('published', 'Published')], default='published', help_text='Only Published events are publicly visible.', max_length=50),
        ),
    ]