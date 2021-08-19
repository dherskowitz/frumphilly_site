from django.contrib import admin
from .models import ForumCategory, ForumThread, ForumPost


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    readonly_fields = ("slug",)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")


admin.site.register(ForumCategory, CategoryAdmin)
admin.site.register(ForumThread, ThreadAdmin)
admin.site.register(ForumPost)
