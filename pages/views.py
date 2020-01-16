from django.shortcuts import render
from pages.models import Page


def home(request):
    page = Page.objects.get(page_name="Home")
    context = {"meta_title": page.meta_title, "meta_description": page.meta_description}
    return render(request, "pages/home.html", context)
