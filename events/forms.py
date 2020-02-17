from django import forms
from .models import Event


class TimeInput(forms.TimeInput):
    input_type = "time"


class EmailInput(forms.EmailInput):
    input_type = "email"


class PhoneInput(forms.TextInput):
    input_type = "tel"


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ("created_by", "slug", "city")

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["start_time"].widget = TimeInput()
        self.fields["start_date"].widget = DateInput()
        self.fields["end_date"].widget = DateInput()
        self.fields["email_contact"].widget = EmailInput()
        self.fields["phone_contact"].widget = PhoneInput()
        self.fields["phone_contact"].widget.attrs[
            "pattern"
        ] = "[0-9]{3}-[0-9]{3}-[0-9]{4}"
        self.fields["image"].widget.attrs["accept"] = "image/png,image/jpg,image/jpeg"

        # Set placeholder for each field
        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = self.fields[
                field
            ].help_text
        self.fields["video"].widget.attrs[
            "placeholder"
        ] = "link to a video about your event."

