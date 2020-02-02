from django.contrib import admin
from .models import Event


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_date",
    )
    ordering = (
        "-start_date",
        "name",
    )
    # list_filter = ("event_in_past",)


admin.site.register(Event, EventAdmin)
