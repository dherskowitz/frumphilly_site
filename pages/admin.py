from django.contrib import admin
from .models import Contact, ReportPost


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
    )
    list_filter = ("subject",)
    readonly_fields = ("created_at",)


class ReportPostAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "post_type",
    )
    list_filter = ("report_reason", "post_type")
    readonly_fields = ("created_at",)


admin.site.register(Contact, ContactAdmin)
admin.site.register(ReportPost, ReportPostAdmin)
