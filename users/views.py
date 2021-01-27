from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event
from listings.models import Listing
from ads.models import Ad
from payments.models import Payment
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
    context = {
        "events": events,
    }
    return render(request, "user/user_events.html", context)


@login_required
def user_listings(request):
    listings = Listing.objects.filter(created_by=request.user).order_by("-created_at", "business_name")
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


@login_required
def admin_review_ads(request):
    ads = Ad.objects.filter(status='review').order_by("-created_at")

    context = {
        "ads": ads,
    }
    return render(request, "admin/ad_review_all.html", context)


@login_required
def admin_review_ad(request, uuid):
    ad = Ad.objects.get(redirect_uuid=uuid)
    payment = Payment.objects.get(ad_uuid=ad.redirect_uuid)

    context = {
        "ad": ad,
        "payment": payment
    }
    return render(request, "admin/ad_review_single.html", context)
