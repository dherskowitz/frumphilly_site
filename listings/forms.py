import bleach
from django import forms
from .models import Listing, Category

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


class ListingFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ListingFilterForm, self).__init__(*args, **kwargs)

        cities = (
            Listing.objects.values_list("city", flat=True).distinct().order_by("city")
        )
        city_choices = [(city, city) for city in cities if city is not None]
        self.fields["city"].choices = city_choices


class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = "__all__"
        exclude = ("created_by", "slug", "claimed", "premium", "approved")

    def __init__(self, *args, **kwargs):
        category_group = kwargs.pop("category_group", [])
        super(ListingForm, self).__init__(*args, **kwargs)
        retail_exclude = ("kashrut",)
        if category_group != "Food & Drink":
            del self.fields["kashrut"]
        elif category_group == "Food & Drink":
            self.fields["kashrut"].required = True

        self.fields["categories"] = forms.ModelMultipleChoiceField(
            queryset=Category.objects.filter(category_group__title=category_group).order_by("title"),
            widget=forms.CheckboxSelectMultiple()
        )

        # Set custom inputs
        self.fields["whatsapp"].widget = PhoneInput()
        self.fields["phone"].widget = PhoneInput()
        self.fields["mobile"].widget = PhoneInput()
        self.fields["email"].widget = EmailInput()
        # self.fields["sun_thu_hours"].widget = TimeInput()
        # self.fields["friday_hours"].widget = TimeInput()
        # self.fields["saturday_hours"].widget = TimeInput()

        # Change labels
        self.fields["sun_thu_hours"].label = "Hours Sun-Thurs"
        self.fields["friday_hours"].label = "Hours Friday"
        self.fields["saturday_hours"].label = "Hours Saturday"
        self.fields["accept_cc"].label = "Accepts Credit Cards"
        self.fields["delivers"].label = "Offers Delivery"
        self.fields["wheelchair_access"].label = "Wheelchair Accessible"

        self.fields["status"].widget.attrs['class'] = "block w-full pl-2 py-4"

        # Hide Fields
        self.fields["city"].label = ""
        self.fields["city"].widget = forms.HiddenInput()
        self.fields["state"].label = ""
        self.fields["state"].widget = forms.HiddenInput()
        self.fields["zipcode"].label = ""
        self.fields["zipcode"].widget = forms.HiddenInput()
        self.fields["location_type"].label = ""
        self.fields["location_type"].widget = forms.HiddenInput()
        self.fields["description"].widget = forms.HiddenInput()

        # add custom error messages
        self.fields["categories"].error_messages.update(
            {"required": "Please select at least one category!"}
        )

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
