# Generated by Django 3.0.2 on 2020-01-16 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20200116_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='meta_description',
            field=models.TextField(help_text='page description for search engines', max_length=150, verbose_name='meta description'),
        ),
        migrations.AlterField(
            model_name='page',
            name='meta_title',
            field=models.CharField(help_text='page title for search engines/tab name/bookmarking', max_length=70, verbose_name='meta title'),
        ),
        migrations.AlterField(
            model_name='page',
            name='page_name',
            field=models.CharField(help_text='name of the page', max_length=50, verbose_name='page name'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='content',
            field=models.TextField(help_text='value for the content', verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='content_name',
            field=models.CharField(help_text='descriptive name for this content', max_length=50, verbose_name='content name'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='page',
            field=models.ForeignKey(help_text='to which page does this belong', on_delete=django.db.models.deletion.CASCADE, to='pages.Page', verbose_name='page name'),
        ),
    ]
