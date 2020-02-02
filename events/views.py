from django.shortcuts import render
from .models import Event
from .forms import EventForm


# Create your views here.
def events_all(request):
    events = Event.objects.order_by("-start_date")
    context = {"events": events}
    return render(request, "pages/events/events_all.html", context)


def events_single(request, event_id):
    event = Event.objects.get(pk=event_id)
    context = {"event": event}
    return render(request, "pages/events/events_single.html", context)


def events_create(request):
    form = EventForm()
    datetime_fields = ("start_date", "end_date")
    context = {"form": form, "datetime_fields": datetime_fields}

    if request.method == "POST":
        form = EventForm(request)
        context["form"] = form

    return render(request, "pages/events/events_create.html", context)
