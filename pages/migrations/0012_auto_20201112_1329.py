# Generated by Django 3.1.3 on 2020-11-12 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20201112_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(choices=[('Advertising', 'Advertising'), ('Feature Request', 'Feature Request'), ('General Inquiry', 'General Inquiry'), ('Suggestion', 'Suggestion'), ('Support', 'Support')], max_length=50),
        ),
    ]
