from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from .models import Ad, ad_prices
from .forms import AdForm
from payments.views import stripe_config


def redirect_ad(request, id):
    ad = Ad.objects.get(redirect_uuid=id)
    return redirect(ad.redirect_to)


@login_required
def create_ad(request):
    form = AdForm()
    context = {"form": form}
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        context["form"] = form

        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect(f"/ads/review/?ad={ad.redirect_uuid}")

    return render(request, 'ads/create.html', context)


@login_required
def edit_ad(request, uuid):
    ad = get_object_or_404(Ad, redirect_uuid=uuid)
    if request.user != ad.user:
        return render(request, "403.html")

    form = AdForm(instance=ad)
    context = {
        "form": form,
        "ad": ad
    }

    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=ad)
        context["form"] = form

        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect(f"/ads/review/?ad={ad.redirect_uuid}")

    return render(request, 'ads/edit.html', context)


@login_required
def review_ad(request):
    uuid = request.GET['ad']
    ad = Ad.objects.filter(redirect_uuid=uuid).first()
    price_info = ad_prices[f"{ad.contract_length}"]
    if request.user != ad.user:
        return render(request, "403.html")
    context = {
        "ad": ad,
        "stripe": stripe_config(request),
        "price_info": price_info
    }
    return render(request, 'ads/review.html', context)