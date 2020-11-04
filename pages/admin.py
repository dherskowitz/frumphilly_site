from django.contrib import admin
from .models import Contact, ReportPost


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
    )
    list_filter = ("subject",)


class ReportPostAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "post_type",
    )
    list_filter = ("report_reason", "post_type")


admin.site.register(Contact, ContactAdmin)
admin.site.register(ReportPost, ReportPostAdmin)
