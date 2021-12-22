import bleach
from django import forms
from .models import Contact, ReportPost, SUBJECT_CHOICES, REPORT_REASON_CHOICES


class EmailInput(forms.EmailInput):
    input_type = "email"


class PhoneInput(forms.TextInput):
    input_type = "tel"


class AdvertisingContactForm(forms.ModelForm):
    subject = forms.ChoiceField(widget=forms.HiddenInput(), initial="Advertising") 

    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "subject", "message")

    def __init__(self, *args, **kwargs):
        super(AdvertisingContactForm, self).__init__(*args, **kwargs)

        self.fields["phone"].widget = PhoneInput()
        self.fields["email"].widget = EmailInput()
        self.fields["subject"].widget.attrs['class'] = "block w-full pl-2 py-4"
        self.fields["message"].widget.attrs['rows'] = "6"
    
    def clean_message(self):
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
        message = self.cleaned_data["message"]
        clean_message = bleach.clean(message, tags=tags, attributes=["href"])
        return clean_message


class ContactForm(forms.ModelForm):
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    class Meta:
        model = Contact
        fields = ("name", "email", "phone", "subject", "message")

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields["phone"].widget = PhoneInput()
        self.fields["email"].widget = EmailInput()
        self.fields["subject"].widget.attrs['class'] = "block w-full pl-2 py-4"
        self.fields["message"].widget.attrs['rows'] = "6"
    
    def clean_message(self):
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
        message = self.cleaned_data["message"]
        clean_message = bleach.clean(message, tags=tags, attributes=["href"])
        return clean_message


class ReportPostForm(forms.ModelForm):
    # subject = forms.ChoiceField(choices=REPORT_REASON_CHOICES)

    class Meta:
        model = ReportPost
        fields = "__all__"
        exclude = ('status',)

    def __init__(self, *args, **kwargs):
        super(ReportPostForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget = EmailInput()
        self.fields["report_reason"].widget.attrs['class'] = "block w-full pl-2 py-4"
        self.fields["message"].widget.attrs['rows'] = "2"

    def clean_message(self):
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
        message = self.cleaned_data["message"]
        clean_message = bleach.clean(message, tags=tags, attributes=["href"])
        return clean_message
