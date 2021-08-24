from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.conf import settings
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "_avatar")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "_avatar")


class CustomUserSettingsForm(UserChangeForm):
    class Meta:
        model = CustomUser
        exclude = ("password",)
        fields = ("first_name", "last_name", "_avatar", "username")

    def __init__(self, *args, **kwargs):
        super(CustomUserSettingsForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if username in settings.ACCOUNT_USERNAME_BLACKLIST:
            raise forms.ValidationError("Username can not be used. Please use other username.")
        return username
