# Generated by Django 3.1.3 on 2021-01-28 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='redirect_uuid',
            field=models.CharField(blank=True, db_index=True, default=None, max_length=100, null=True),
        ),
    ]