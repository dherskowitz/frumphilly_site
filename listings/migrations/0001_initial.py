# Generated by Django 3.0.2 on 2020-07-19 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(default='', help_text='What is the name of this business?', max_length=200)),
                ('website', models.URLField(blank=True, default='', help_text='Enter the URL of your website if you have one.', null=True)),
                ('facebook', models.URLField(blank=True, default='', help_text='Enter the URL of your Facebook page if you have one.', null=True)),
                ('twitter', models.URLField(blank=True, default='', help_text='Enter the URL of your Twitter page if you have one.', null=True)),
                ('instagram', models.URLField(blank=True, default='', help_text='Enter the URL of your Instagram page if you have one.', null=True)),
                ('whatsapp', models.CharField(blank=True, default=None, help_text='Enter your WhatsApp number if you have one.', max_length=18, null=True)),
                ('phone', models.CharField(blank=True, default=None, help_text='Enter your Phone number.', max_length=18, null=True)),
                ('mobile', models.CharField(blank=True, default=None, help_text='Enter your mobile number.', max_length=18, null=True)),
                ('fax', models.CharField(blank=True, default=None, help_text='Enter your Fax number.', max_length=18, null=True)),
                ('email', models.EmailField(blank=True, default=None, help_text='Enter your email address if you have one.', max_length=254, null=True)),
                ('location', models.CharField(help_text='Enter the Address of your business', max_length=500)),
                ('city', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('state', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('zipcode', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('location_type', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('summary', models.CharField(blank=True, default=None, help_text='120 character description of your business', max_length=120, null=True)),
                ('description', models.TextField(blank=True, default=None, help_text='Full description of your business', null=True)),
                ('kashrut', models.CharField(blank=True, default=None, help_text='If you are a food business what Kashrut do you have.', max_length=120, null=True)),
                ('sun_thu_hours', models.CharField(blank=True, default=None, help_text='What are your hours Sun-Thurs.', max_length=120, null=True)),
                ('friday_hours', models.CharField(blank=True, default=None, help_text='What are your hours on Friday.', max_length=120, null=True)),
                ('saturday_hours', models.CharField(blank=True, default=None, help_text='What are your hours Saturday (if any).', max_length=120, null=True)),
                ('claimed', models.BooleanField(default=False)),
                ('premium', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('accept_cc', models.BooleanField(default=False)),
                ('wheelchair_access', models.BooleanField(default=False)),
                ('slug', models.SlugField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(to='listings.Category')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='listings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'listing',
                'verbose_name_plural': 'listings',
            },
        ),
    ]
