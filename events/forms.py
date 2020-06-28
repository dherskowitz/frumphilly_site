import requests
import bleach
from decouple import config
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Event


FILE_CONTENT_TYPES = ["pdf"]
IMAGE_CONTENT_TYPES = ["image"]
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 5242880


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
        exclude = ("created_by", "slug")

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
        self.fields["attachment"].widget.attrs["accept"] = "application/pdf"

        # Hidden fields
        self.fields["suburb"].label = ""
        self.fields["suburb"].widget = forms.HiddenInput()
        self.fields["city"].label = ""
        self.fields["city"].widget = forms.HiddenInput()
        self.fields["state"].label = ""
        self.fields["state"].widget = forms.HiddenInput()
        self.fields["description"].widget = forms.HiddenInput()

        # Set placeholder for each field
        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = self.fields[
                field
            ].help_text
        self.fields["video"].widget.attrs[
            "placeholder"
        ] = "Link to a video about your event."
        self.fields["phone_contact"].widget.attrs[
            "placeholder"
        ] = "Where can people call for more info"
        self.fields["link"].widget.attrs[
            "placeholder"
        ] = "Requires full URL e.g. http://example.com"
        self.fields["cost"].widget.attrs[
            "placeholder"
        ] = "If your event has a cost to attend."

    def clean_attachment(self):
        attachment = self.cleaned_data["attachment"]
        if hasattr(attachment, "content_type"):
            content_type = attachment.content_type.split("/")[1]
            if content_type in FILE_CONTENT_TYPES:
                if attachment.size > MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(
                        _("Attachment file must be less than 5MB.")
                    )
            else:
                raise forms.ValidationError("Attachment only accepts PDF files.")
        return attachment

    def clean_image(self):
        image = self.cleaned_data["image"]
        if hasattr(image, "content_type"):
            content_type = image.content_type.split("/")[0]
            if content_type not in IMAGE_CONTENT_TYPES:
                raise forms.ValidationError(
                    _("Image must be (jpg, jpeg, png, gif) format.")
                )
        return image

    def clean_location(self):
        location = self.cleaned_data["location"]
        base_url = "https://api.geocod.io/v1.6/geocode"
        api_key = config("GEOCODING_KEY")
        req = requests.get(f"{base_url}?q={location}&api_key={api_key}")
        data = req.json()
        if "error" in data:
            raise forms.ValidationError(
                _("Please enter a valid US address in location.")
            )
        return data["results"][0]["formatted_address"]

    def clean_description(self):
        tags = [
            "h1",
            "div",
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "strong",
            "ul",
            "br",
            "del",
        ]
        description = self.cleaned_data["description"]
        clean_description = bleach.clean(description, tags=tags, attributes=["href"])
        print("============")
        print(description)
        print(clean_description)
        return clean_description
