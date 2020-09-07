from django.contrib import admin
from .models import Event


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
        "created_at",
        "created_by",
    )
    ordering = (
        "-start_date",
        "-created_at",
        "name",
    )
    search_fields = ("name", "created_by__id")
    # list_filter = ("event_in_past",)


admin.site.register(Event, EventAdmin)
