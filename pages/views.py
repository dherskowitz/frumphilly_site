from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event


def home(request):
    # page_meta = Page.objects.get(page_name="Home")
    # page_content = PageContent.objects.filter(page=page_meta.id)
    # page_data = {}
    # for page_item in page_content:
    #     page_data[page_item.content_name] = page_item.content
    upcoming_events = Event.get_upcoming_events()
    events_in_future = True
    if len(upcoming_events) == 0:
        upcoming_events = Event.objects.all().order_by("-start_date")[:10]
        events_in_future = False
    context = {
        # "page_data": page_data,
        # "page_meta": page_meta,
        "upcoming_events": upcoming_events,
        "events_in_future": events_in_future,
    }
    return render(request, "pages/site/home.html", context)


def about(request):
    return render(request, "pages/site/about.html")


def contact(request):
    return HttpResponse("Contact page")


def terms(request):
    return render(request, "pages/site/terms.html")


def privacy(request):
    return render(request, "pages/site/privacy.html")
