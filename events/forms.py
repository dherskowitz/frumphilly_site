from django import forms
from .models import Event


class TimeInput(forms.TimeInput):
    input_type = "time"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("created_by",)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].widget = TimeInput()
