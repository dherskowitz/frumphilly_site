import bleach
from django import forms
from .models import Ad

IMAGE_CONTENT_TYPES = ["jpeg", "jpg", "png", "gif"]
MAX_UPLOAD_SIZE = 104857600


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ("type","title","image","contract_length","redirect_to", "read_terms")

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data["title"]
        clean_title = bleach.clean(title)
        return clean_title

    def clean_read_terms(self):
        read_terms = self.cleaned_data["read_terms"]
        if not read_terms:
            raise forms.ValidationError("You must agree to the terms to continue.")
        return read_terms

    def clean_image(self):
        image = self.cleaned_data["image"]
        if hasattr(image, "content_type"):
            content_type = image.content_type.split("/")[1]
            if content_type in IMAGE_CONTENT_TYPES:
                if image.size > MAX_UPLOAD_SIZE:
                    raise forms.ValidationError("Image must be less than 100MB.")
            else:
                raise forms.ValidationError("Image only accepts jpg/jpeg/gif/png files.")
        else:
            raise forms.ValidationError("An Image is required.")
        return image
