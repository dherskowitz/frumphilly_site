from django.contrib import admin
from .models import Ad


class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "contract_length", "status")
    list_filter = ("contract_length", "status", "type")
    # readonly_fields = ("slug",)


admin.site.register(Ad, AdAdmin)
