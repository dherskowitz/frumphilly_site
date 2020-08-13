from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from events.models import Event
from listings.models import Listing


# Create your views here.
@login_required
def user_account(request):
    return render(request, "user/user_account.html")


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
