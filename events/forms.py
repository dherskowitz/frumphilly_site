from django import forms
from .models import Event


class TimeInput(forms.TimeInput):
    input_type = "time"


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("created_by",)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].widget = TimeInput()
        self.fields["start_date"].widget = DateInput()
        self.fields["end_date"].widget = DateInput()

        # Set placeholder for each field
        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = self.fields[field].help_text
