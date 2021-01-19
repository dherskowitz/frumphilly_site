import bleach
from django import forms
from .models import Ad

FILE_CONTENT_TYPES = ["pdf"]
MAX_UPLOAD_SIZE = 104857600

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ("type","title","image","contract_length","redirect_to")

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
