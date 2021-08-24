import bleach
from django import forms
from .models import ForumThread, ForumPost

FILE_CONTENT_TYPES = ["pdf"]
IMAGE_CONTENT_TYPES = ["image"]
MAX_UPLOAD_SIZE = 5242880


class ThreadCreateForm(forms.ModelForm):

    class Meta:
        model = ForumThread
        fields = "__all__"
        exclude = ("author", "slug", "category")

    def __init__(self, *args, **kwargs):
        super(ThreadCreateForm, self).__init__(*args, **kwargs)


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = ForumPost
        fields = "__all__"
        exclude = ("author", "slug", "category", "thread")

    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)

    def clean_content(self):
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
        content = self.cleaned_data["content"]
        clean_content = bleach.clean(content, tags=tags, attributes=["href"])
        return clean_content
