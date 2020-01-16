from django.contrib import admin
from .models import Page, PageContent


# Register your models here.
class PageAdmin(admin.ModelAdmin):
    model = Page
    list_display = [
        "page_name",
    ]


class PageContentAdmin(admin.ModelAdmin):
    model = PageContent
    list_display = [
        "page",
        "content_name",
    ]


admin.site.register(Page, PageAdmin)
admin.site.register(PageContent, PageContentAdmin)
