from django.shortcuts import render
from pages.models import Page, PageContent
from events.models import Event


def home(request):
    page_meta = Page.objects.get(page_name="Home")
    page_content = PageContent.objects.filter(page=page_meta.id)
    page_data = {}
    for page_item in page_content:
        page_data[page_item.content_name] = page_item.content
    upcoming_events = Event.get_upcoming_events()
    context = {
        "page_data": page_data,
        "page_meta": page_meta,
        "upcoming_events": upcoming_events,
    }
    return render(request, "pages/home.html", context)
