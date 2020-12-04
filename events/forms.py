import requests
import bleach
from decouple import config
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Event, EventCategory


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
MAX_UPLOAD_SIZE = 104857600


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


class EventFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EventFilterForm, self).__init__(*args, **kwargs)
        cities = Event.objects.filter(status='Published').values_list('city', flat=True).distinct().order_by('city')
        city_choices = [(city, city) for city in cities if city is not None]
        self.fields['city'].choices = city_choices


class EventForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=EventCategory.objects.all().order_by("title"), widget=forms.CheckboxSelectMultiple
    )

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

        self.fields["status"].widget.attrs['class'] = "block w-full pl-2 py-4"

        # Hidden fields
        self.fields["city"].label = ""
        self.fields["city"].widget = forms.HiddenInput()
        self.fields["state"].label = ""
        self.fields["state"].widget = forms.HiddenInput()
        self.fields["zipcode"].label = ""
        self.fields["zipcode"].widget = forms.HiddenInput()
        self.fields["location_type"].label = ""
        self.fields["location_type"].widget = forms.HiddenInput()
        self.fields["description"].widget = forms.HiddenInput()

        self.fields["categories"].error_messages.update(
            {"required": "Please select at least one category!"}
        )

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
            if content_type in FILE_CONTENT_TYPES:
                if image.size > MAX_UPLOAD_SIZE:
                    raise forms.ValidationError(
                        _("Attachment file must be less than 100MB.")
                    )
            if content_type not in IMAGE_CONTENT_TYPES:
                raise forms.ValidationError(
                    _("Image must be (jpg, jpeg, png, gif) format.")
                )
        return image

    def clean(self):
        link = self.cleaned_data["link"]
        location = self.cleaned_data["location"]
        virtual = self.cleaned_data["is_virtual_event"]
        if not virtual and not location:
            raise forms.ValidationError(
                _("A location is required for non-virtual events.")
            )
        if virtual and not link:
            raise forms.ValidationError(
                _("A link is required for virtual events.")
            )
        return self.cleaned_data


    # def clean_location(self):
    #     """ Validate address using additional geolocation """
    #     location = self.cleaned_data["location"]
    #     base_url = "https://api.geocod.io/v1.6/geocode"
    #     api_key = config("GEOCODING_KEY")
    #     req = requests.get(f"{base_url}?q={location}&api_key={api_key}")
    #     data = req.json()
    #     if "error" in data:
    #         raise forms.ValidationError(
    #             _(
    #                 "Please enter a valid US address in location. (Including city and state)"
    #             )
    #         )
    #     if len(data["results"]) == 0:
    #         raise forms.ValidationError(
    #             _(
    #                 "Please enter a valid US address in location. (Including city and state)"
    #             )
    #         )
    #     return self.cleaned_data["location"]

    def clean_description(self):
        tags = [
            "h1",
            "p",
            "div",
            "a",
            "abbr",
            "acronym",
            "b",
            "blockquote",
            "table",
            "tbody",
            "tr",
            "td",
            "code",
            "em",
            "i",
            "li",
            "ol",
            "strong",
            "ul",
            "br",
            "del",
            "pre",
        ]
        description = self.cleaned_data["description"]
        clean_description = bleach.clean(description, tags=tags, attributes=["href"])
        return clean_description
