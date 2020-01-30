from django.forms import ModelForm
from . import models


class EventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = ["name", "image"]
