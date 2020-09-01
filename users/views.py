from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from events.models import Event
from listings.models import Listing
from .models import CustomUser


# Create your views here.
@login_required
def user_account(request):
    context = {
        "events_count": CustomUser.get_events_count(),
        "listings_count": CustomUser.get_listings_count(),
    }
    return render(request, "user/user_account.html", context)


@login_required
def user_events(request):
    events = Event.objects.filter(created_by=request.user)
    context = {
        "events": events,
    }
    return render(request, "user/user_events.html", context)


@login_required
def user_listings(request):
    listings = Listing.objects.filter(created_by=request.user)
    context = {
        "listings": listings,
    }
    return render(request, "user/user_listings.html", context)
