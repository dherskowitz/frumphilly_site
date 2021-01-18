from django.contrib import admin
from .models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "contract_length", "status", "type")
    list_filter = ("contract_length", "status", "type")
    read_only = ("redirect_uuid")


admin.site.register(Ad, AdAdmin)
