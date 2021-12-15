from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ads.models import Ad, ad_prices
from pages.models import Contact
from payments.models import Payment


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
    payments = Payment.objects.filter(ad_uuid=ad.redirect_uuid)
    price_info = ad_prices[f"{ad.contract_length}"]

    context = {
        "ad": ad,
        "payments": payments,
        "price_info": price_info
    }
    return render(request, "admin/ad_review_single.html", context)


@login_required
def admin_all_ads(request):
    context = {
        "ads": Ad.objects.all().order_by("-created_at")
    }
    return render(request, "admin/ads_all.html", context)
