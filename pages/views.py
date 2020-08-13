from django.shortcuts import render
from events.models import Event


def home(request):
    upcoming_events = Event.get_upcoming_events()
    events_in_future = True
    if len(upcoming_events) == 0:
        upcoming_events = Event.objects.all().order_by("-start_date")[:10]
        events_in_future = False
    context = {
        "upcoming_events": upcoming_events,
        "events_in_future": events_in_future,
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")


def contact(request):
    return render(request, "pages/contact.html")


def terms(request):
    return render(request, "pages/terms.html")


def privacy(request):
    return render(request, "pages/privacy.html")
