from django.db import models


class PageContent(models.Model):
    page = models.ForeignKey(
        "Page",
        verbose_name="page name",
        help_text="To which page does this belong",
        on_delete=models.CASCADE,
        related_name="page",
    )
    content_name = models.CharField(
        verbose_name="content name",
        help_text="Descriptive name for this content with word separated by underscores (e.g. main_title)",
        max_length=50,
    )
    content = models.TextField(
        verbose_name="content", help_text="Value for the content"
    )

    class Meta:
        verbose_name = "Page Content"
        verbose_name_plural = "Page Contents"

    def __str__(self):
        return self.page.page_name


class Page(models.Model):
    page_name = models.CharField(
        verbose_name="page name", help_text="Name of the page", max_length=50
    )
    meta_title = models.CharField(
        verbose_name="meta title",
        help_text="Page title for search engines/tab name/bookmarking",
        max_length=70,
    )
    meta_description = models.TextField(
        verbose_name="meta description",
        help_text="Page description for search engines",
        max_length=150,
    )

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.page_name
