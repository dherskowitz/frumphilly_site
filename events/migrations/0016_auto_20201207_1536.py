# Generated by Django 3.1.3 on 2020-12-07 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_event_neighborhood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('draft', 'Save for Later'), ('published', 'Published')], default='published', help_text='Events will not show until Published', max_length=50),
        ),
    ]
