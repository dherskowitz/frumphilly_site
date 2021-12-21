import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
from decouple import config
from pages.forms import ReportPostForm
from .models import Listing, CategoryGroup, Category
from .forms import ListingForm
from ads.models import Ad


def listings_all(request, category=None):
    ads = Ad.get_active_ads()
    listings = Listing.objects.all().order_by("-created_at").filter(status='published')
    cities = listings.values_list('city', flat=True).distinct().order_by('city')
    # categories = Category.objects.all(category_group=listing_group).order_by('title')
    categories = CategoryGroup.objects.all().order_by('title')
    subcategories = None
    filtered_cities = request.GET.getlist('location')
    if filtered_cities:
        listings = listings.filter(city__in=filtered_cities)

    filtered_categories = request.GET.getlist('category')
    if filtered_categories:
        subcategories = [x.title for x in
                         Category.objects.filter(category_group__title=filtered_categories[0]).order_by('title')]
        listings = listings.distinct().filter(categories__title__in=subcategories)

    filtered_subcategories = request.GET.getlist('subcategory')
    if filtered_subcategories:
        listings = listings.filter(categories__title__in=filtered_subcategories)

    page = request.GET.get("page", 1)
    paginator = Paginator(listings, 10)
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        listings = paginator.page(1)
    except EmptyPage:
        listings = paginator.page(paginator.num_pages)

    context = {
        "listings": listings,
        "cities": cities,
        "categories": categories,
        "subcategories": subcategories,
        "category_group": "Listings",
        "filtered_cities": filtered_cities,
        "filtered_categories": filtered_categories,
        "filtered_subcategories": filtered_subcategories,
        "ads": ads,
    }

    return render(request, "listings/index.html", context)


# def listings(request, slug):
#     listing_group = CategoryGroup.objects.filter(slug=slug).get()

#     listings = Listing.get_listings_by_group(slug)
#     cities = listings.values_list('city', flat=True).distinct().order_by('city')
#     categories = Category.objects.filter(category_group=listing_group).order_by('title')

#     # Set category group in request for use in forms
#     if not request.GET._mutable:
#         request.GET._mutable = True
#     request.GET['cat_group'] = slug
#     request.GET._mutable = False

#     filtered_cities = request.GET.getlist('location')
#     if filtered_cities:
#         listings = listings.filter(city__in=filtered_cities)

#     filtered_categories = request.GET.getlist('category')
#     if filtered_categories:
#         listings = listings.filter(categories__title__in=filtered_categories)

#     page = request.GET.get("page", 1)
#     paginator = Paginator(listings, 10)
#     try:
#         listings = paginator.page(page)
#     except PageNotAnInteger:
#         listings = paginator.page(1)
#     except EmptyPage:
#         listings = paginator.page(paginator.num_pages)

#     context = {
#         "listings": listings,
#         "cities": cities,
#         "categories": categories,
#         "category_group": listing_group.title,
#         "filtered_cities": filtered_cities,
#         "filtered_categories": filtered_categories,
#     }

#     return render(request, "listings/index.html", context)


def listing_single(request, slug, pk):
    ads = Ad.get_active_ads()
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    user_liked = listing.is_liked_by(request.user)
    if listing.status == 'draft' and request.user != listing.created_by:
        return render(request, "private.html")
    report_post_form = ReportPostForm()
    categories = [{"title": cat.title, "category_group": cat.category_group.title} for cat in listing.categories.all()]
    context = {"listing": listing, "categories": categories, "report_post_form": report_post_form, "ads": ads,
               "user_liked": user_liked}
    return render(request, "listings/single.html", context)


@login_required
def listings_create(request, slug):
    category_group = get_object_or_404(CategoryGroup, slug=slug)
    form = ListingForm(category_group=category_group.title)
    check_fields = [
        "claimed",
        "premium",
        "approved",
        "accept_cc",
        "delivers",
        "wheelchair_access",
    ]
    context = {"form": form, "check_fields": check_fields, "mapbox": config("MAPBOX_KEY")}
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, category_group=category_group.title)
        context["form"] = form

        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.save()
            form.save_m2m()
            messages.success(request, "Listing created successfully!")
            return redirect("/user/listings/")
    context["category_group"] = category_group
    return render(request, "listings/create.html", context)


@login_required
def listings_edit(request, slug, pk):
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    category_group = CategoryGroup.objects.filter(
        title=listing.categories.first().category_group
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
    context = {"form": form, "check_fields": check_fields, "listing": listing, "mapbox": config("MAPBOX_KEY")}
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
            return redirect("/user/listings/")

    return render(request, "listings/edit.html", context)


@login_required
def listings_delete(request, slug, pk):
    listing = get_object_or_404(Listing, slug=slug, id=pk)
    if request.user != listing.created_by:
        return render(request, "403.html")
    context = {"listing": listing}
    if request.method == "POST":
        listing.delete()
        messages.success(request, f'Listing {listing.business_name} was deleted successfully!')
        return redirect("/user/listings/")
    return render(request, "listings/delete.html", context)


@login_required
def listings_select(request):
    context = {"options": CategoryGroup.get_all_listing_types()}
    return render(request, "listings/select.html", context)


def listing_categories(request):
    return {'nav_categories': CategoryGroup.objects.all().order_by("title")}


# def listings_category(request, slug):
#     listings_list = Listing.get_listings_by_group(slug)
#     if not request.GET._mutable:
#         request.GET._mutable = True
#     request.GET['cat_group'] = slug
#     request.GET._mutable = False
#     listings_filter = ListingsFilter(request.GET, request=request, queryset=listings_list)
#     listings_list = listings_filter.qs
#     page = request.GET.get("page", 1)
#     paginator = Paginator(listings_list, 10)
#     try:
#         listings = paginator.page(page)
#     except PageNotAnInteger:
#         listings = paginator.page(1)
#     except EmptyPage:
#         listings = paginator.page(paginator.num_pages)

#     context = {
#         "filtered_cities": request.GET.getlist("city"),
#         "filtered_categories": request.GET.getlist("categories"),
#         "filter": listings_filter,
#         "listings": listings,
#     }
#     return render(request, "listings/index.html", context)

# @csrf_exempt
def listing_like(request, listing_id):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseForbidden()
    listing = get_object_or_404(Listing, id=listing_id)

    if listing.is_liked_by(current_user):
        listing.dislike(current_user)
    else:
        listing.like(current_user)

    context = {
        "user_liked": listing.is_liked_by(request.user),
        "listing": listing,
    }

    return render(request, "listings/_like.html", context)

