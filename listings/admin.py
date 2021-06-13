from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import Listing, Category, CategoryGroup


def make_published(modeladmin, request, queryset):
    queryset.update(status='published')


make_published.short_description = "Mark selected listings as published"


def make_draft(modeladmin, request, queryset):
    queryset.update(status='draft')


make_draft.short_description = "Mark selected listings as draft"


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    def likes_count(self, obj):
        return obj.likes.count()

    actions = [make_published, make_draft]
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    readonly_fields = ("slug", "created_by", "likes_count")
    list_display = (
        "business_name",
        "created_at",
        "status",
        "created_by",
    )
    exclude = ('likes',)
    # ordering = (
    #     "-start_date",
    #     "-created_at",
    #     "name",
    # )
    # search_fields = ('name', 'created_by__id')
    list_filter = ("status", "categories__category_group")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category_group")
    list_filter = ("category_group",)
    readonly_fields = ("slug",)


class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = ("title",)
    readonly_fields = ("slug",)


admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryGroup, CategoryGroupAdmin)
