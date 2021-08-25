from django.contrib import admin
from .models import ForumCategory, ForumThread, ForumPost


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    readonly_fields = ("slug",)


class ThreadAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")


class PostsAdmin(admin.ModelAdmin):
    list_display = ("title",)

    @staticmethod
    def title(obj):
        return f"{obj.author.email} replied to {obj.thread.title} at {obj.created_at}"


admin.site.register(ForumCategory, CategoryAdmin)
admin.site.register(ForumThread, ThreadAdmin)
admin.site.register(ForumPost, PostsAdmin)
