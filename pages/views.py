import json
import bleach
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from honeypot.decorators import check_honeypot
from events.models import Event
from listings.models import Listing
from forum.models import ForumPost, ForumThread
from .models import ReportPost
from .forms import ContactForm, AdvertisingContactForm, ReportPostForm
from ads.models import Ad


def home(request):
    ads = Ad.get_active_ads()
    listings = Listing.objects.filter(status="published").order_by("-created_at")[:15]
    upcoming_events = Event.get_upcoming_events()
    latest_forum_activity = ForumThread.get_latest()
    context = {
        "ads": ads,
        "listings": listings,
        "upcoming_events": upcoming_events,
        "latest_forum_activity": latest_forum_activity
    }
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")


@check_honeypot(field_name='last_name')
def contact(request):
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_obj = form.save(commit=False)
            contact_obj.save()
            messages.success(request, "Your message was sent sucessfully!")
            return redirect(home)
    context = {
        "form": form
    }
    return render(request, "pages/contact.html", context)


@check_honeypot(field_name='last_name')
def advertising(request):
    form = AdvertisingContactForm()

    if request.method == "POST":
        form = AdvertisingContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.success(request, "Your message was sent sucessfully!")
            return redirect(home)
    context = {
        "form": form
    }
    return render(request, "pages/advertising.html", context)


def terms(request):
    return render(request, "pages/terms.html")


def privacy(request):
    return render(request, "pages/privacy.html")


def ad_terms(request):
    return render(request, "pages/ad-terms.html")


def report_post(request):
    if request.method == "POST":
        post_type = request.POST.get("post_type")
        post_id = request.POST.get("post_id")
    else:
        post_type = request.GET.get("post_type")
        post_id = request.GET.get("post_id")

    if post_type == 'Listing':
        obj = get_object_or_404(Listing, id=post_id)
    elif post_type == 'Event':
        obj = get_object_or_404(Event, id=post_id)

    form = ReportPostForm(request.POST or None)
    context = {
        "form": form,
        "post": obj
    }

    if request.method == "POST":
        if form.is_valid():
            report = form.save(commit=False)
            if request.user.is_authenticated:
                report.user_id = request.user.id
                report.email = request.user.email
            report.save()
            return render(request, "components/reported_success.html", context)
        return render(request, "components/report_post_modal.html", context)
    return render(request, "components/report_post_modal.html", context)
