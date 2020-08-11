from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Listing, Category
from .forms import ListingForm


def listings(request):
    listings = Listing.get_listings()
    context = {"listings": listings}
    return render(request, "listings/index.html", context)


def listing_single(request, slug, pk):
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    context = {"listing": listing}
    return render(request, "listings/single.html", context)


def listings_category(request, slug):
    category = Category.get_category_by_slug(slug)
    listings = Listing.get_listings_by_category(slug)
    context = {"listings": listings, "category": category}
    return render(request, "listings/category.html", context)


@login_required
def listings_create(request):
    form = ListingForm()
    check_fields = [
        "claimed",
        "premium",
        "approved",
        "accept_cc",
        "delivers",
        "wheelchair_access",
    ]
    context = {"form": form, "check_fields": check_fields}
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            messages.success(request, "Listing created successfully!")
            return redirect(listing_single, slug=listing.slug, pk=listing.id)

    return render(request, "listings/create.html", context)


@login_required
def listings_edit(request, slug, pk):
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    if request.user != listing.created_by:
        return render(request, "403.html")
    form = ListingForm(instance=listing)
    check_fields = [
        "claimed",
        "premium",
        "approved",
        "accept_cc",
        "delivers",
        "wheelchair_access",
    ]
    context = {"form": form, "check_fields": check_fields, "listing": listing}
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        context["form"] = form

        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            form.save_m2m()
            messages.success(request, "Listing updated successfully!")
            return redirect(listing_single, slug=listing.slug, pk=listing.id)

    return render(request, "listings/edit.html", context)


@login_required
def listings_delete(request, slug, pk):
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    if request.user != listing.created_by:
        return render(request, "403.html")
    context = {"listing": listing}
    if request.method == "POST":
        listing.delete()
        return redirect(listings)
    return render(request, "listings/delete.html", context)
