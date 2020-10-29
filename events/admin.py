from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import Event, EventCategory


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {"widget": CheckboxSelectMultiple},
    }
    list_display = (
        "name",
        "event_categories",
        "created_by",
    )
    ordering = (
        "-start_date",
        "-created_at",
        "name",
    )
    readonly_fields = ("slug", "created_by")
    search_fields = ("name", "created_by__id")
    list_filter = ("categories",)

    def event_categories(self, obj):
        return ", ".join([p.title for p in obj.categories.all()])


class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")


admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
