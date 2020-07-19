from django.shortcuts import render
from .models import Listing


def listings(request):
    listings = Listing.get_listings()
    context = {"listings": listings}
    return render(request, "listings/index.html", context)
