# Generated by Django 3.0.2 on 2020-01-22 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20200116_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='meta_description',
            field=models.TextField(help_text='Page description for search engines', max_length=150, verbose_name='meta description'),
        ),
        migrations.AlterField(
            model_name='page',
            name='meta_title',
            field=models.CharField(help_text='Page title for search engines/tab name/bookmarking', max_length=70, verbose_name='meta title'),
        ),
        migrations.AlterField(
            model_name='page',
            name='page_name',
            field=models.CharField(help_text='Name of the page', max_length=50, verbose_name='page name'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='content',
            field=models.TextField(help_text='Value for the content', verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='content_name',
            field=models.CharField(help_text='Descriptive name for this content with word separated by underscores (e.g. main_title)', max_length=50, verbose_name='content name'),
        ),
        migrations.AlterField(
            model_name='pagecontent',
            name='page',
            field=models.ForeignKey(help_text='To which page does this belong', on_delete=django.db.models.deletion.CASCADE, to='pages.Page', verbose_name='page name'),
        ),
    ]
