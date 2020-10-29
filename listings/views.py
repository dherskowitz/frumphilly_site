from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Listing, CategoryGroup
from .forms import ListingForm
from .filters import ListingsFilter


def listings(request):
    listings_list = Listing.objects.all()
    listings_filter = ListingsFilter(request.GET, request=request, queryset=listings_list)
    listings_list = listings_filter.qs
    page = request.GET.get("page", 1)
    paginator = Paginator(listings_list, 10)
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    context = {
        "filtered_cities": request.GET.getlist("city"),
        "filtered_categories": request.GET.getlist("categories"),
        "filter": listings_filter,
        "listings": listings,
    }

    return render(request, "listings/index.html", context)


def listing_single(request, slug, pk):
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    context = {"listing": listing}
    return render(request, "listings/single.html", context)


@login_required
def listings_create(request, slug):
    category_group = get_object_or_404(CategoryGroup, slug=slug)
    form = ListingForm(category_group=category_group.slug)
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
            form.save_m2m()
            messages.success(request, "Listing created successfully!")
            return redirect(listing_single, slug=listing.slug, pk=listing.id)
    context["category_group"] = category_group
    return render(request, "listings/create.html", context)


@login_required
def listings_edit(request, slug, pk):
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    category_group = CategoryGroup.objects.filter(
        title=listing.categories.first()
    ).first()
    if request.user != listing.created_by:
        return render(request, "403.html")
    form = ListingForm(instance=listing, category_group=category_group)
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
        form = ListingForm(
            request.POST, request.FILES, instance=listing, category_group=category_group
        )
        context["form"] = form

        if form.is_valid():
            listing = form.save(commit=False)
            # listing.created_by = request.user
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


@login_required
def listings_select(request):
    context = {"options": CategoryGroup.get_all_listing_types()}
    return render(request, "listings/select.html", context)
