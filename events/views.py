from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Event
from .forms import EventForm


# Create your views here.
def events_all(request):
    events = Event.objects.order_by("-start_date")
    context = {"events": events}
    return render(request, "pages/events/events_all.html", context)


def events_single(request, slug):
    event = Event.objects.get(slug=slug)
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
        return redirect(events_all)

    return render(request, "pages/events/events_create.html", context)


@login_required
def events_edit(request, slug):
    event = Event.objects.get(slug=slug)
    if request.user != event.created_by:
        return HttpResponseForbidden()
    form = EventForm(instance=event)
    datetime_fields = ("start_date", "end_date")
    context = {"form": form, "event": event, "datetime_fields": datetime_fields}

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        context["form"] = form

        if form.is_valid():
            event_edit = form.save(commit=False)
            event_edit.created_by = request.user
            event_edit.save()
        return redirect(events_single, slug=event.slug)

    return render(request, "pages/events/events_edit.html", context)


@login_required
def events_delete(request, slug):
    event = Event.objects.get(slug=slug)
    if request.user != event.created_by:
        return HttpResponseForbidden()
    context = {"event": event}
    if request.method == "POST":
        event.delete()
        return redirect(events_all)
    return render(request, "pages/events/events_delete.html", context)
