# Generated by Django 3.0.2 on 2020-09-03 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0009_auto_20200903_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.CategoryGroup'),
        ),
    ]