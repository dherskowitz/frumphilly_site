from django.shortcuts import render, get_object_or_404
from .models import Listing


def listings(request):
    listings = Listing.get_listings()
    context = {"listings": listings}
    return render(request, "listings/index.html", context)


def listing_single(request, slug, pk):
    print(slug, pk)
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    context = {"listing": listing}
    return render(request, "listings/single.html", context)
