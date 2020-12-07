# Generated by Django 3.1.3 on 2020-12-07 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0023_listing_neighborhood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('draft', 'Save for Later'), ('published', 'Published')], default='published', help_text='Listings will not show until Published', max_length=50),
        ),
    ]
