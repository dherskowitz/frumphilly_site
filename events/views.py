from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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


@login_required
def events_create(request):
    form = EventForm()
    datetime_fields = ("start_date", "end_date")
    context = {"form": form, "datetime_fields": datetime_fields}

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()

    return render(request, "pages/events/events_create.html", context)
