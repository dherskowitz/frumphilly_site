from django.contrib import admin
from .models import Listing, Category


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
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
    list_display = ("title",)


admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
