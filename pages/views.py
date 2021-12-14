import json
import bleach
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from honeypot.decorators import check_honeypot
from events.models import Event
from listings.models import Listing
from forum.models import ForumPost, ForumThread
from .models import ReportPost
from .forms import ContactForm, AdvertisingContactForm
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
            contact = form.save(commit=False)
            contact.save()
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


@require_POST
def report_post(request):
    data = json.loads(request.body)

    missing = []
    for field in data:
        if data[field] == "":
            missing.append(field)

    missing_auto_fields = []
    if 'post_type' in missing:
        missing_auto_fields.append('post_type')
    if 'post_id' in missing:
        missing_auto_fields.append('post_id')
    if 'post_title' in missing:
        missing_auto_fields.append('post_title')

    if 'report_reason' in missing:
        return JsonResponse({"status": "errors", "errors": ['Report Reason is required']}, status=400)
    elif missing_auto_fields:
        return JsonResponse({"status": "errors", "errors": ['Something went wrong. Please refresh the page and try again.']}, status=400)
    else:
        report = ReportPost()
        report.post_type = data['post_type']
        report.post_id = data['post_id']
        report.post_title = data['post_title']
        report.message = bleach.clean(data['message'])
        report.report_reason = data['report_reason']
        report.email = data['email']
        if request.user.is_authenticated:
            report.user_id = request.user.id
            report.email = request.user.email
        report.save()
        return JsonResponse({"status": "success"}, status=200)
