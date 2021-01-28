from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decouple import config
from .models import Event, EventCategory
from .forms import EventForm
from .filters import EventFilter
from pages.forms import ReportPostForm
from ads.models import Ad


helptext_fields = (
    "start_date",
    "end_date",
    "rsvp",
    "image",
    "attachment",
    "video",
    "start_time",
    "cost",
    "link",
)


# Create your views here.
def events_all(request):
    ads = Ad.get_active_ads()
    events_list = Event.objects.filter(status="published").order_by("-start_date", "-start_time")
    cities = events_list.values_list('city', flat=True).distinct().order_by('city')
    categories = EventCategory.objects.all().order_by('title')

    filtered_cities = request.GET.getlist('location')
    if filtered_cities:
        events_list = events_list.filter(city__in=filtered_cities)

    filtered_categories = request.GET.getlist('category')
    if filtered_categories:
        events_list = events_list.filter(categories__title__in=filtered_categories)

    page = request.GET.get("page", 1)
    paginator = Paginator(events_list, 10)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    context = {
        "events": events,
        "cities": cities,
        "categories": categories,
        "filtered_cities": filtered_cities,
        "filtered_categories": filtered_categories,
        "ads": ads
    }
    return render(request, "events/index.html", context)


def events_single(request, slug, pk):
    ads = Ad.get_active_ads()
    event = get_object_or_404(Event, slug=slug, id=pk)
    if event.status == 'draft' and request.user != event.created_by:
        return render(request, "private.html")
    report_post_form = ReportPostForm()
    context = {"event": event, "report_post_form": report_post_form, "ads": ads}
    return render(request, "events/single.html", context)


@login_required
def events_create(request):
    form = EventForm()
    context = {"form": form, "helptext_fields": helptext_fields, "mapbox": config("MAPBOX_KEY")}

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            form.save_m2m()
            messages.success(request, "Event created successfully!")
            return redirect("/user/events/")

    return render(request, "events/create.html", context)


@login_required
def events_edit(request, slug, pk):
    event = get_object_or_404(Event, slug=slug, id=pk)
    if request.user != event.created_by:
        return render(request, "403.html")
    form = EventForm(instance=event)
    datetime_fields = ("start_date", "end_date")
    context = {
        "form": form,
        "event": event,
        "datetime_fields": datetime_fields,
        "helptext_fields": helptext_fields,
        "mapbox": config("MAPBOX_KEY")
    }

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        context["form"] = form

        if form.is_valid():
            event_edit = form.save(commit=False)
            # event_edit.created_by = request.user
            event_edit.save()
            form.save_m2m()
            messages.success(request, "Event updated successfully!")
            return redirect(events_single, slug=event.slug, pk=event.id)

    return render(request, "events/edit.html", context)


@login_required
def events_delete(request, slug, pk):
    event = get_object_or_404(Event, slug=slug, id=pk)
    if request.user != event.created_by:
        return render(request, "403.html")
    context = {"event": event}
    if request.method == "POST":
        event.delete()
        messages.success(request, f'Event {event.name} was deleted successfully!')
        return redirect("/user/events/")
    return render(request, "events/delete.html", context)
