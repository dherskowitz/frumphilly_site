import bleach
from django import forms
from .models import ForumThread, ForumPost
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

FILE_CONTENT_TYPES = ["pdf"]
IMAGE_CONTENT_TYPES = ["image"]
MAX_UPLOAD_SIZE = 5242880

allowed_tags = [
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
    "img",
    "s",
    "u",
    "hr"
]
allowed_attrs = {'a': ['href', 'rel'], 'img': ['src', 'alt', 'style']}
styles = ["width", "height", "border-color", "background-color", "white-space", "vertical-align", "text-align",
          "border-style", "border-width", "float", "margin", "margin-bottom", "margin-left", "margin-right",
          "margin-top"]


class ThreadCreateForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = ForumThread
        fields = "__all__"
        exclude = ("author", "slug", "category")

    def __init__(self, *args, **kwargs):
        super(ThreadCreateForm, self).__init__(*args, **kwargs)

    def clean_content(self):
        content = self.cleaned_data["content"]
        clean_content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, styles=styles)
        return clean_content


class PostCreateForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = ForumPost
        fields = "__all__"
        exclude = ("author", "slug", "category", "thread")

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)

    def clean_content(self):
        content = self.cleaned_data["content"]
        clean_content = bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, styles=styles)
        return clean_content
