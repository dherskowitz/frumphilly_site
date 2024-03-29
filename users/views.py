from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from listings.models import Listing
from ads.models import Ad
from .models import CustomUser
from .forms import CustomUserSettingsForm


# Create your views here.
@login_required
def user_account(request):
    context = {
        "events_count": CustomUser.get_events_count(request),
        "listings_count": CustomUser.get_listings_count(request),
        "ads_count": CustomUser.get_ads_count(request),
    }
    return render(request, "user/user_account.html", context)


@login_required
def user_settings(request):
    user = CustomUser.get_user_settings(request.user)
    context = {"form": CustomUserSettingsForm(instance=user)}
    if request.method == "POST":
        form = CustomUserSettingsForm(request.POST, request.FILES, instance=user)
        context["form"] = form
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            form.save_m2m()
            messages.success(request, "User updated successfully!")
            return redirect("user_settings")
    return render(request, "user/user_settings.html", context)


@login_required
def user_events(request):
    events = Event.objects.filter(created_by=request.user).order_by("-created_at", "name")

    page = request.GET.get("page", 1)
    paginator = Paginator(events, 15)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {
        "events": events,
    }
    return render(request, "user/user_events.html", context)


@login_required
def user_listings(request):
    listings = Listing.objects.filter(created_by=request.user).order_by("-created_at", "business_name")

    page = request.GET.get("page", 1)
    paginator = Paginator(listings, 12)
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    context = {
        "listings": listings,
    }
    return render(request, "user/user_listings.html", context)


@login_required
def user_ads(request):
    ads = Ad.objects.filter(user=request.user).order_by("status")
    context = {
        "ads": ads,
    }
    return render(request, "user/user_ads.html", context)

