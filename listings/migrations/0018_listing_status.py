# Generated by Django 3.1.3 on 2020-11-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0017_auto_20201102_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='status',
            field=models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published')], default='Published', max_length=50),
        ),
    ]