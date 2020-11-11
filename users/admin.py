from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "_avatar")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Groups", {"fields": ("groups",)}),
        ("User Permissions", {"fields": ("user_permissions",)},),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2", "_avatar")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
