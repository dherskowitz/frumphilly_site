from django.contrib import admin
from .models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "contract_length", "status", "type", "clicks")
    list_filter = ("contract_length", "status", "type")
    readonly_fields = ("redirect_uuid", "created_at", "image_type", "clicks")


admin.site.register(Ad, AdAdmin)
