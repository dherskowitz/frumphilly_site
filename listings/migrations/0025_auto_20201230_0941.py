# Generated by Django 3.1.3 on 2020-12-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0024_auto_20201207_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='categorygroup',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('draft', 'Save for Later'), ('published', 'Published')], default='published', help_text='Only Published listings are publicly visible.', max_length=50),
        ),
    ]
