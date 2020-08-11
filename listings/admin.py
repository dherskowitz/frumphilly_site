from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import Listing, Category


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    readonly_fields = ("slug", "created_by")
    list_display = (
        "business_name",
        "created_at",
        "created_by",
    )
    # ordering = (
    #     "-start_date",
    #     "-created_at",
    #     "name",
    # )
    # search_fields = ('name', 'created_by__id')
    # list_filter = ("event_in_past",)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    readonly_fields = ("slug",)


admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
