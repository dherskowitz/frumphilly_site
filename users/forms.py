from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "avatar")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "avatar")


class CustomUserSettingsForm(UserChangeForm):
    class Meta:
        model = CustomUser
        exclude = ("password",)
        fields = ("first_name", "last_name", "avatar")
