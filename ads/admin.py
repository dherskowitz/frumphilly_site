from django.contrib import admin
from .models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "contract_length", "status", "type")
    list_filter = ("contract_length", "status", "type")
    readonly_fields = ("redirect_uuid", "created_at",)


admin.site.register(Ad, AdAdmin)
